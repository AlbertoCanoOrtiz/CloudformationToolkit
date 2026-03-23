# Gmail MCP Server — AWS Serverless Deployment

> 🤖 *Architecture and CloudFormation templates improved by [Amazon Q](https://aws.amazon.com/q/developer/)*

A serverless implementation of the [Gmail MCP Server](https://github.com/AlbertoCanoOrtiz/GmailMCP) built with AWS Lambda, API Gateway, and S3.

---

## Architecture

```
Client  →  API Gateway (ANY /gmailMCP)  →  Lambda (Python 3.11)  →  FastMCP (Gmail API)
                                               ↑
                                         Lambda Layer
                                      (MCP server code)
```

| File | Purpose |
|---|---|
| `dogsjgp-gmail-iam-segurity&roles.yaml` | IAM role and S3 access policy |
| `dogsjgp-gmail-lambda-core.yaml` | Lambda function + Layer |
| `dogsjgp-gmail-gateway-mcp.yaml` | HTTP API Gateway |
| `lambda_handler.py` | Lambda bootstrap entrypoint |

---

## Prerequisites

- AWS CLI configured with sufficient permissions
- An S3 bucket named `ogsjgp-gmail-mcp-server`
- Gmail OAuth credentials (`token.json` and `dogsjgp_dev_gcp_gmail_mcp_server.json`)
- Python 3.11

---

## Step by Step Deployment

### Step 1 — Clone the MCP server source

```bash
git clone https://github.com/AlbertoCanoOrtiz/GmailMCP.git
cd GmailMCP
```

### Step 2 — Install dependencies into the source folder

```bash
pip install -r src/utils/requirements.txt -t src/
```

### Step 3 — Generate the OAuth token

```bash
python src/utils/utils.py
```

> This will create `token.json` in your secrets folder. Keep it safe.

### Step 4 — Package the MCP server as a zip for the Lambda Layer

The zip must have `src/` at the root level so imports resolve correctly.

```bash
zip -r ogsjgp-gmail-mcp-server.zip src/
```

### Step 5 — Package the Lambda handler

```bash
zip lambda_handler.zip lambda_handler.py
```

### Step 6 — Upload both zips to S3

```bash
aws s3 cp ogsjgp-gmail-mcp-server.zip s3://ogsjgp-gmail-mcp-server/ogsjgp-gmail-mcp-server.zip
aws s3 cp lambda_handler.zip s3://ogsjgp-gmail-mcp-server/lambda_handler.zip
```

### Step 7 — Deploy the IAM stack

```bash
aws cloudformation deploy \
  --template-file dogsjgp-gmail-iam-segurity\&roles.yaml \
  --stack-name dogsjgp-gmail-iam \
  --capabilities CAPABILITY_NAMED_IAM
```

### Step 8 — Deploy the Lambda stack

```bash
aws cloudformation deploy \
  --template-file dogsjgp-gmail-lambda-core.yaml \
  --stack-name dogsjgp-gmail-lambda \
  --capabilities CAPABILITY_IAM
```

### Step 9 — Deploy the API Gateway stack

```bash
aws cloudformation deploy \
  --template-file dogsjgp-gmail-gateway-mcp.yaml \
  --stack-name dogsjgp-gmail-gateway
```

### Step 10 — Get the endpoint URL

```bash
aws cloudformation describe-stacks \
  --stack-name dogsjgp-gmail-gateway \
  --query "Stacks[0].Outputs[?OutputKey=='McpEndpoint'].OutputValue" \
  --output text
```

Your MCP server will be available at:
```
https://<api-id>.execute-api.<region>.amazonaws.com/prod/gmailMCP
```

---

## Teardown

Delete stacks in reverse order:

```bash
aws cloudformation delete-stack --stack-name dogsjgp-gmail-gateway
aws cloudformation delete-stack --stack-name dogsjgp-gmail-lambda
aws cloudformation delete-stack --stack-name dogsjgp-gmail-iam
```

---

## Stack Parameters

All stacks use parameters with sensible defaults so you can override without editing the templates:

```bash
aws cloudformation deploy \
  --template-file dogsjgp-gmail-iam-segurity\&roles.yaml \
  --stack-name dogsjgp-gmail-iam \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides S3BucketName=my-custom-bucket
```
