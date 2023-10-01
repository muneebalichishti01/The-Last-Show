# The Last Show - Obituary Generator Application

In this project, I created a full stack application with one group partner, QAZI ALI, with React and AWS that generates obituaries for people (fictional or otherwise). We used [ChatGPT](https://openai.com/blog/chatgpt) to generate an obituary, [Amazon Polly](https://aws.amazon.com/polly/) to turn the obituary into speech, and [Cloudinary](https://cloudinary.com/) to store the speech and a picture of the deceased (may they rest in peace).

## Architecture Overview

<br/>
<p align="center">
  <img src="https://res.cloudinary.com/mkf/image/upload/v1680411648/last-show_dvjjez.svg" alt="the-last-show-architecture" width="800"/>
</p>
<br/>

## :foot: Steps

- Make sure you're inside the root directory of the repo and then run `npm install` to install all the necessary packages
- Run `npm start` and you should be able to see the page open up on your default browser

## :computer: Details
- Added infrastructure code in the `main.tf` file
- Added function code for the `get-obituaries-<ucid>` function in the [`functions/get-obituaries/main.py`](functions/get-obituaries/main.py) file
- Added function code for the `create-obituary-<ucid>` function in the [`functions/create-obituary/main.py`](functions/create-obituary/main.py) file

## :page_with_curl: Notes

- Created all the resources on AWS with Terraform. All configurations are put in in the [`main.tf`](infra/main.tf) file
- Used AWS DynamoDB for the database
- Used [Lambda Function URLs](https://masoudkarimif.github.io/posts/aws-lambda-function-url/) for this project to connect the backend to the frontend
- Created 2 Lambda functions for this project:

  - `get-obituaries-<ucid>`: to retrieve all the obituaries. Function URL only allows `GET` requests
  - `create-obituary-<ucid>`: to create a new obituary. The function reads all the data (including the picture) from the body of the request. Function URL only allows `POST` requests

- Used Python to write the functions
- Orchestrated different steps of the `create-obituary` Lambda function with [AWS Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html). 4 Lambda functions:
  - `generate-obituary` that uses ChatGPT
  - `read-obituary` that uses Amazon Polly
  - `store-files` that uses Cloudinary to store both the picture and speech
  - `save-item` that uses DynamoDB to store a new item
  (created all the infra using Terraform)

- The only external libraries used in the functions are [`requests`](https://pypi.org/project/requests/) for sending HTTPS requests to ChatGPT and Cloudinary, and [requests-toolbelt](https://pypi.org/project/requests-toolbelt/) for decoding the body of the request received from the front-end. No other external libraries are used
- Used the [Cloudinary Upload API](https://cloudinary.com/documentation/image_upload_api_reference) and **not the SDK** to interact with Cloudinary
- Used the [ChatGPT API](https://platform.openai.com/docs/api-reference/making-requests) and **not the SDK** to interact with ChatGPT
- Used [AWS Systems Manager Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html) and the `SecureString` data type to store the keys for my Cloudinary and ChatGPT accounts. The `create-obituary` Lambda function will read the keys from the Parameter Store using the `boto3` library. The keys are not be present in the application or infra code in the repo. These keys are created using the AWS CLI and manually on the AWS Console
- Used [Amazon Polly](https://aws.amazon.com/polly/) to turn the obituary written by ChatGPT to speech and then upload the `mp3` version of that to Cloudinary
- ChatGPT API usage: limit of `max_tokens` set to 600

## :couple: Group Assignment

- This is a grouped project, and I worked with QAZI ALI on this assignment
- We both worked on the front-end and back-end of the application
- We both worked on the infrastructure code
- We both worked on the function code

## :clap: Acknowledgements

- [AWS Lambda Function URLs](https://masoudkarimif.github.io/posts/aws-lambda-function-url/)
- [Cloudinary Upload API](https://cloudinary.com/documentation/image_upload_api_reference)
- [ChatGPT API](https://platform.openai.com/docs/api-reference/making-requests)
- [AWS Systems Manager Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html)
- [Amazon Polly](https://aws.amazon.com/polly/)
- [AWS Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html)
- [requests](https://pypi.org/project/requests/)
- [requests-toolbelt](https://pypi.org/project/requests-toolbelt/)
