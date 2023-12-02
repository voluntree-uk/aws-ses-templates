import argparse
import os
import logging
import yaml
import boto3

def parse_args():
    parser = argparse.ArgumentParser(description='Registers AWS SES templates.')
    parser.add_argument('src', metavar='SOURCE', type=str, default='templates.yaml', help='A path to the templates config file')
    parser.add_argument('--aws-profile', type=str, default=os.environ.get('AWS_PROFILE'), help='An AWS of the target account')
    parser.add_argument('--aws-region', type=str, default=os.environ.get('AWS_REGION'), help='An AWS region of the target account')
    return parser.parse_args()

def setup_logger():
    logger=logging.getLogger()
    logger.setLevel(logging.INFO)

    stream_handler=logging.StreamHandler()
    stream_formatter=logging.Formatter(
        """{"ts":"%(asctime)s", "name": "%(name)s", "level": "%(levelname)s", "message": "%(message)s"}""",
        "%Y-%m-%dT%H:%M:%SZ"
    )
    stream_handler.setFormatter(stream_formatter)

    logger.addHandler(stream_handler)
    return logger

def register_template(template, ses_client, logger):
    config = {
        'TemplateName': template["name"],
        'SubjectPart': template["subject"],
        'HtmlPart': open(template["source"], 'r').read()
    }
    try:
        exists = ses_client.get_template(TemplateName=template["name"])
        if exists:
            logger.info(f'Template "{template["name"]}" already exist. Updating...')
            ses_client.update_template(Template = config)
            logger.info(f'...updated')
    except boto3.botocore.errorfactory.TemplateDoesNotExistException:
        logger.info(f'Template "{template["name"]}" does not exist. Creating...')
        ses_client.create_template(Template=config)
        logger.info(f'...created')
    except:
        logger.error(f'Unexpected error occurred when registering template {template["name"]}')

def main():
  logger = setup_logger()
  args = parse_args()
  
  logger.info(f'Starting the application with arguments: {args}')

  logger.info('Initialising AWS SDK...')
  ses_client = boto3.session.Session(profile_name=args.aws_profile, region_name=args.aws_region).client('ses')
  logger.info('...AWS SDK initialised')

  logger.info(f'Loading templates configurations from {args.src}')
  with open(args.src, 'r') as file:
      source = yaml.safe_load(file)
      for template in source['templates']:
          register_template(template, ses_client, logger)
  logger.info('All templates successfully registered')


if __name__ == "__main__":
    main()