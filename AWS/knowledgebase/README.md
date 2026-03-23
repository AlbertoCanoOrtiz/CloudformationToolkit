# Bedrock Image Knowledge Base - Coast People

> 🤖 Architecture and CloudFormation templates improved by Amazon Q

CloudFormation template that provisions an Amazon Bedrock Knowledge Base backed by OpenSearch Serverless for image vector search, deployed within a VPC.

## Resources

| Resource | Type | Description |
|---|---|---|
| `UnderscoreImageOpensearchCoastpeopleai` | `AWS::OpenSearchServerless::Collection` | Vector search collection |
| `UnderscoreImageOpensearchCoastpeopleaiVpcendpoint` | `AWS::OpenSearchServerless::VpcEndpoint` | VPC endpoint for private access |
| `UnderscoreImageBedrockCoastpeopleai` | `AWS::Bedrock::KnowledgeBase` | Bedrock Knowledge Base using Nova multimodal embeddings |

## Parameters

| Parameter | Default | Description |
|---|---|---|
| `KnowledgeBaseName` | `underscore-image-bedrock-coastpeopleoai` | Name of the Bedrock Knowledge Base |
| `RoleARN` | — | IAM Service Role ARN for Bedrock execution |
| `VpcId` | — | VPC where the endpoint will be deployed |
| `SubnetIds` | — | Subnets for the VPC endpoint |
| `SecurityGroupIds` | — | Security groups for the VPC endpoint |
| `VectorIndexName` | `image-opensearch-coastpeople` | OpenSearch index name |
| `VectorField` | `image-vector-embeddings` | Field to store vector embeddings |
| `TextField` | `image-vector-text` | Field to store text content |
| `MetadataField` | `image-vector-metadata` | Field to store metadata |

## Embedding Model

Uses **Amazon Nova Multimodal Embeddings v1** (`amazon.nova-multimodal-embeddings-v1:0`) for generating image and text vector embeddings.

## Deploy

```bash
aws cloudformation deploy \
  --template-file dogsjgp-image-knowledgebase-coastpeople.yaml \
  --stack-name image-knowledgebase-coastpeople \
  --parameter-overrides \
      RoleARN=<your-bedrock-role-arn> \
      VpcId=<your-vpc-id> \
      SubnetIds=<subnet-id-1>,<subnet-id-2> \
      SecurityGroupIds=<sg-id> \
  --capabilities CAPABILITY_NAMED_IAM
```
