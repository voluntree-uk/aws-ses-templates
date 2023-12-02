# AWS SES Template Manager

This software is used to create and update the AWS SES email templates. 

These emails are transactional emails used by the Voluntree platform.

All email templates need to be in HTML format.

## Config File

A required source config file is a yaml file listing email template configurations. 

Each template needs to configure the following properties:


| Property | Description                                       | 
|----------|---------------------------------------------------|
| name     | Template name                                     | 
| subject  | A default subject line                            |
| source   | A relative file path to the template body in HTML |
| data     | A list of data parameters                         |

Note that the `data` template parameters are listed for documentation purposes only.

## Template Editor

The email templates are located in the `templates/` directory and can be edited locally 
or using an email HTML editor such as [semplates](app.semplates.io). 

[Semplates](app.semplates.io) provides a featureful, free HTML editor that supports 
exports which can then be added to the local templates list and registered using the script.


## Usage 

```
usage: python3 register.py [-h] [--aws-profile AWS_PROFILE] [--aws-region AWS_REGION] SOURCE

Registers AWS SES templates.

positional arguments:
  SOURCE                A path to the templates config file

options:
  -h, --help            show this help message and exit
  --aws-profile AWS_PROFILE
                        An AWS of the target account
  --aws-region AWS_REGION
                        An AWS region of the target account

```
