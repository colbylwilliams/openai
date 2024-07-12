param name string

param user string

param location string = resourceGroup().location

// Cognitive Services OpenAI Contributor
var openAIContributorRoleId = subscriptionResourceId(
  'Microsoft.Authorization/roleDefinitions',
  'a001fd3d-188f-4b5d-821b-7da978bf7442'
)

resource openai 'Microsoft.CognitiveServices/accounts@2024-04-01-preview' = {
  name: name
  location: location
  kind: 'OpenAI'
  sku: {
    name: 'S0'
  }
  properties: {
    customSubDomainName: name
    disableLocalAuth: true
  }
}

resource gpt_4o 'Microsoft.CognitiveServices/accounts/deployments@2024-04-01-preview' = {
  name: 'gpt-4o'
  parent: openai
  sku: {
    name: 'Standard'
    capacity: 150
  }
  properties: {
    model: {
      format: 'OpenAI'
      name: 'gpt-4o'
      version: '2024-05-13'
    }
  }
}

resource text_embedding_3_large 'Microsoft.CognitiveServices/accounts/deployments@2024-04-01-preview' = {
  name: 'text-embedding-3-large'
  parent: openai
  sku: {
    name: 'Standard'
    capacity: 150
  }
  properties: {
    model: {
      format: 'OpenAI'
      name: 'text-embedding-3-large'
      version: '1'
    }
  }
}

// Cognitive Services OpenAI Contributor
resource role_assignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(openai.id, user, openAIContributorRoleId)
  scope: openai
  properties: {
    principalId: user
    principalType: 'User'
    roleDefinitionId: openAIContributorRoleId
  }
}

output endpoint string = openai.properties.endpoint
