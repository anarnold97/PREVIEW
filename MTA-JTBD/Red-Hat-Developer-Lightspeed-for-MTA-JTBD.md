# Red Hat Developer Lightspeed for MTA

---

## Discover

*JTBD Statement: When I am exploring application modernization tools, I want to understand how AI-assisted refactoring conceptually works, so that I can determine if this solution meets my organization's needs.*

### Product overview

*JTBD Statement: "When I am modernizing application portfolios, I want to use AI-driven code suggestions that improve as more migration data becomes available, so that I can resolve complex code issues with increasing accuracy and minimal manual effort."*

Starting from version 8.0.0, the Migration Toolkit for Applications (MTA) integrates with large language models (LLMs) through the Red Hat Developer Lightspeed for MTA Visual Studio Code extension.

The extension works by collecting and storing code changes across a large collection of applications, finding context to generate prompts for your preferred LLM, and outputting code resolutions to address migration issues.

Red Hat Developer Lightspeed for MTA uses Retrieval Augmented Generation (RAG) to produce context-based resolutions for issues in your code. By employing RAG, the extension improves the context shared with the LLM as more migration data becomes available, producing more accurate fix suggestions over time.

### Use cases for AI-driven code fixes

*JTBD Statement: "When I am performing static code analysis across a large portfolio of applications , I want the LLM to use the 2,400+ rule definitions and issue descriptions to generate relevant fix suggestions , so that I can avoid duplicate work and resolve migration issues more efficiently."*

MTA performs static code analysis for a specified target technology. Red Hat provides over 2,400 analysis rules for various migration targets.

The static code analysis describes specific issues in your code that require resolution. When performing an analysis across a large portfolio of applications, the issue descriptions and rule definitions provide the LLM with the context it needs to generate relevant fix suggestions.

### Context definition for large language models

*JTBD Statement: "When I am resolving modernization issues, I want to provide the LLM with comprehensive context including source code, rules, and past solutions, so that the model can generate reliable and accurate fix suggestions."*

The context supplied to the LLM is a combination of:

- **Issue descriptions:** Descriptions of the issues detected by MTA when running a static code analysis for a set of target technologies.
- **Rule information:** Optional additional information included in default and custom rules that helps Red Hat Developer Lightspeed define the context.
- **Solved examples:** Code changes from previous migrations that form a resolution pattern for future use. A solved example is generated when a user accepts a resolution in a previous analysis that updates a file to resolve an issue.

Solved examples are stored in the Solution Server. A higher volume of solved examples for a specific issue enhances the overall context and improves the success metrics of the rules that trigger that issue type.

If enabled, the Solution Server extracts a resolution pattern — referred to as a "migration hint" — that the LLM uses to generate a more accurate fix suggestion in future analyses.

### Solution Server

*JTBD Statement: "When I am modernizing a large portfolio of applications, I want to leverage a shared organizational memory of successful code fixes and real-world success metrics, so that I can resolve recurring issues with high confidence and avoid redundant manual effort."*

The Solution Server is a component that enables Red Hat Developer Lightspeed for MTA to build a collective memory of source code changes from every analysis performed within an organization.

The Solution Server augments previous patterns of source code changes (solved examples) that are similar to the current file, and suggests a resolution with a higher confidence level derived from prior successful fixes.

The Solution Server delivers two primary benefits:

- **Contextual Hints:** Surfaces examples of past migration solutions (including successful user modifications and accepted fixes) to offer actionable hints for difficult or previously unsolved migration issues.
- **Migration Success Metrics:** Exposes detailed success metrics for each migration rule based on real-world usage data. IDEs or automation tools can use these metrics to present users with a "confidence level" before they apply a code fix.

When using the Solution Server, you can view a diff between the updated portions of the code and the original source code to perform a manual review. During the review, you can accept, reject, or edit the suggested resolutions.

### Agent AI

*JTBD Statement: "When I need to resolve code issues in a specific file without running a full hub analysis, I want to use an autonomous AI agent to plan, execute, and iteratively refine fixes, so that I can automatically resolve both migration and diagnostic issues until the code is fully modernized."*

You can enable either Agent AI mode or Solution Server mode to request AI-assisted code resolutions. In Agent AI mode, Red Hat Developer Lightspeed for MTA streams an automated analysis of a file to identify issues and suggest resolutions, without requiring a prior hub analysis.

In the initial run, the AI agent:

1. Plans the context to define the issues.
2. Chooses a suitable sub-agent for the analysis task, working alongside the LLM to generate fix suggestions, and displays the reasoning transcript along with the files to be changed.
3. Applies the changes to the code once you approve the updates.

If you accept that the agent must continue making changes, it compiles the code and runs a partial analysis. In this iteration, the agent attempts to fix diagnostic issues generated by the compiler or your IDE toolchain. After each iteration, the agent asks if you want it to continue fixing additional issues. When accepted, it runs another iteration until it has successfully resolved all issues.

### Benefits of AI-assisted application migration

*JTBD Statement: "When I am establishing a modernization strategy for large-scale application portfolios, I want to adopt a standardized, platform-led approach to AI-assisted refactoring, so that I can achieve efficient and scalable code migrations using a flexible tool that learns from my data without requiring model fine-tuning."*

Red Hat Developer Lightspeed for MTA provides LLM configuration control and a platform engineering approach to standardize AI-assisted refactoring efforts for large organizational codebases.

- **Model agnostic:** The extension follows a "Bring Your Own Model" approach, allowing your organization to use a preferred LLM.
- **Iterative refinement:** The tool includes an agent that iterates through the source code to run a series of automated analyses, resolving both base code and diagnostic issues.
- **Contextual code generation:** By using AI for static code analysis, the extension breaks down complex problems into manageable pieces, giving the LLM focused context to generate meaningful fix suggestions.
- **No fine-tuning required:** You do not need to fine-tune your model with a specialized dataset for analysis, leaving you free to use and swap LLM models to respond to changing requirements.
- **Learning and improvement:** As more segments of a codebase are migrated, the tool uses RAG to learn from available data and give better recommendations in later analyses.

---

## Get started

*JTBD Statement: "When I have the extension installed, I want to perform a basic scan and generate a single code fix, so that I can quickly learn how to be productive with the tool."*

### Install the IDE extension

*JTBD Statement: "When I am setting up my development environment for application modernization, I want to install the MTA extension from the Visual Studio Code Marketplace, so that I can perform code analysis and access AI-assisted resolutions within my IDE."*

You can install the MTA Visual Studio Code extension from the Visual Studio Code Marketplace. Use the extension to perform analysis and optionally enable Red Hat Developer Lightspeed for MTA for AI-assisted code fixes.

> **Note:** If you change any configuration after enabling the generative AI settings in the extension, you must restart the extension for the change to take effect.

### Generate a code fix suggestion

*JTBD Statement: "When I am modernizing a Java application to Quarkus, I want to use the Agent AI mode to automatically identify issues and generate code fixes, so that I can iteratively resolve migration and diagnostic issues until my code is successfully modernized."*

This example walks you through generating code fixes for a Java application being migrated to Quarkus, using Agent AI mode.

**Prerequisites**

- You installed the MTA Visual Studio Code extension.
- You have an LLM API key for a supported provider.

**Procedure**

1. Open your Java project in Visual Studio Code.
2. Type **Ctrl+Shift+P** (Windows/Linux) or **Cmd+Shift+P** (Mac) to open the Command Palette.
3. Type **Preferences: Open Settings (UI)** and go to **Extensions > MTA**.
4. Select **Gen AI: Agent Mode**.
5. In the Red Hat Developer Lightspeed for MTA extension, click **Open Analysis View**.
6. Type **MTA: Manage Analysis Profile** in the Command Palette and configure the following fields:
   - **Profile Name:** Enter a name for the profile.
   - **Target Technologies:** `quarkus`
   - **Custom Rules:** Select custom rules if required. By default, Red Hat Developer Lightspeed for MTA enables **Use Default Rules** for Quarkus.
7. Type **MTA: Open the Gen AI model provider configuration file** in the Command Palette to open the `provider-settings` file. Configure the active provider. For example, for a model deployed on OpenShift AI:

   ```yaml
   models:
     openshift-example-model: &active
       environment:
         OPENAI_API_KEY: "<Server's OPENAI_API_KEY>"
         CA_BUNDLE: "<Server's CA Bundle path>"
       provider: "ChatOpenAI"
       args:
         model: "my-model"
         configuration:
           baseURL: "https://<serving-name>-<data-science-project-name>.apps.konveyor-ai.example.com/v1"
   ```

   Change the provider configuration if you plan to use a different LLM provider. See [Configure LLM provider settings](#configure-llm-provider-settings).

8. On the **MTA: Open Analysis View** page, click **Start** to start the MTA Remote Procedure Call (RPC) server.
9. Select the profile you configured and click **Run Analysis** to scan the Java application. MTA identifies the issues in the code.
10. Click the solutions icon on an issue to request suggestions. Red Hat Developer Lightspeed for MTA streams the issue description, a preview of the code changes, and the files to be updated.
11. Review the code changes in the editor and click **Accept** or **Reject**. If you accept the changes, Red Hat Developer Lightspeed for MTA creates a new file with the accepted code.
12. Click **Continue** to allow Red Hat Developer Lightspeed for MTA to run a follow-up analysis. This analysis detects lint issues, compilation issues, or diagnostic issues that may have occurred when applying the previous changes.
13. Repeat the review and accept or reject the resolutions. Red Hat Developer Lightspeed for MTA continues to run repeated iterations until all issues are resolved.

---

## Plan

*JTBD Statement: "When I am preparing for a large-scale deployment, I want to evaluate LLM providers and system requirements, so that I can choose the right architecture before committing to an installation."*

### Deployment strategy

To use the features in Red Hat Developer Lightspeed for MTA, you require a Red Hat Advanced Developer Suite (RHADS) subscription.

You can configure Red Hat Developer Lightspeed for MTA in two ways:

- **LLM proxy mode:** Connect the MTA extension to the LLM through the LLM proxy service. The proxy enables Solution Server mode, which shares organizational migration history across users.
- **Agent AI mode (direct connection):** Connect the extension directly to the LLM without the proxy. This mode uses Agent AI for code resolutions and does not require the proxy service.

Choose the LLM proxy mode if you want to enable the Solution Server for your organization. Choose direct Agent AI mode if you want a simpler setup without the proxy.

### Prerequisites for generative AI features

*JTBD Statement: "When I am preparing to use AI-assisted migration features, I want to verify and install the necessary system dependencies and infrastructure components, so that I can ensure my environment is fully compatible and ready for the MTA extension."*

Before you install Red Hat Developer Lightspeed for MTA, ensure that the following prerequisites are met:

- Install the Language Support for Java™ by Red Hat extension.
- Install Java v17 or later.
- Install Maven v3.9.9 or later.
- Install Git and add it to the `$PATH` variable.
- Install the MTA Operator 8.0.0.
- Create an API key for an LLM.

The MTA Operator is required if you plan to enable the Solution Server. It enables you to log in to the `openshift-mta` project and configure the LLM through the Tackle custom resource (CR).

### Persistent volume requirements

*JTBD Statement: "When I am preparing the infrastructure for the Solution Server, I want to create a 5Gi ReadWriteOnce (RWO) persistent volume, so that I have the necessary backend storage to maintain the collective memory of code changes from my analyses."*

The Solution Server requires a backend database to store code changes from previous analyses. If you plan to enable the Solution Server, you must create a 5Gi ReadWriteOnce (RWO) persistent volume used by the Red Hat Developer Lightspeed for MTA database.

### Supported LLM providers

*JTBD Statement: "When I am planning my migration architecture, I want to verify which LLM providers and models are compatible with the extension, so that I can leverage my existing AI infrastructure or select a supported provider that meets my organizational standards."*

The availability of public LLM models is maintained by the respective LLM provider. For a full list of supported providers and example model configurations, see [Configurable Large Language Models and providers](#configurable-large-language-models-and-providers) in the Reference section.

---

## Configure

*JTBD Statement: "When I have my environment ready, I want to connect the extension to my chosen LLM and adjust my IDE and profile settings, so that the tool behaves according to my specific requirements."*

Red Hat Developer Lightspeed for MTA requires the following configurations:

- A Kubernetes secret for the LLM API key (Administrator task)
- The Tackle custom resource (CR) configured for the LLM provider and, optionally, the LLM proxy and Solution Server (Administrator task)
- The `provider-settings.yaml` file configured with the active LLM provider (Migrator task)
- Visual Studio Code IDE settings with LLM credentials (Migrator task)
- An analysis profile that defines the target technology and rules (Migrator task)

### Connect without the LLM proxy (Agent AI mode)

*JTBD Statement: "When I want to use Agent AI mode without a proxy service, I want to configure the LLM provider and model directly in the cluster and activate the extension settings, so that I can generate AI-assisted code resolutions while maintaining a direct connection to my chosen model."*

Use this workflow when you want to use Agent AI mode without the proxy service.

**Administrator tasks:**

1. Create a Kubernetes secret for your LLM key in the Red Hat OpenShift cluster. See [Configure the model secret key](#configure-the-model-secret-key).
2. In the Tackle CR, configure the LLM provider and the LLM model. See [Enable LLM proxy in the Tackle custom resource](#enable-llm-proxy-in-the-tackle-custom-resource).

**Migrator tasks:**

1. Enable generative AI in the MTA extension settings. See [Configure IDE settings](#configure-ide-settings).
2. Configure a profile for the analysis. See [Configure analysis profile settings](#configure-analysis-profile-settings).
3. Activate the LLM provider in the `provider-settings.yaml` file. See [Configure LLM provider settings](#configure-llm-provider-settings).
4. Enable Agent AI and run an analysis to request a code fix suggestion. See [Generate code resolutions in Agent mode](#generate-code-resolutions-in-agent-mode).

### Connect through the LLM proxy service

*JTBD Statement: "When I am setting up the MTA extension to work with Large Language Models in an enterprise environment, I want to connect through a managed LLM proxy service, so that I can centralize credential management and securely enable AI-assisted resolutions across my organization."*

The LLM proxy allows client endpoints — for example, the MTA Visual Studio Code extension — to access LLMs through a centrally managed proxy. The client uses Keycloak credentials to authenticate to the MTA Hub. To authenticate to the LLM, the client sends a JSON Web Token (JWT) issued by Keycloak to the proxy service. The proxy service validates the client's JWT against the Hub's Keycloak instance. The proxy then completes a separate authentication process to access the LLM using the cluster secret that the Administrator configured, allowing Administrators to create, manage, and rotate LLM API keys without sharing them with individual client endpoints.

After enabling the LLM proxy, you can use either the Solution Server or Agent AI to generate code resolution requests in the IDE extension. To use the Solution Server, the Administrator must deploy it in the Tackle CR.

**Administrator tasks:**

1. Create a Kubernetes secret for your LLM key in the Red Hat OpenShift cluster. See [Configure the model secret key](#configure-the-model-secret-key).
2. In the Tackle CR, enable the LLM proxy service, enable the Solution Server (if required), and configure the LLM provider and model. See [Enable LLM proxy in the Tackle custom resource](#enable-llm-proxy-in-the-tackle-custom-resource).

**Migrator tasks:**

1. Enable generative AI in the MTA extension settings. See [Configure IDE settings](#configure-ide-settings).
2. To use Agent AI: enable Agent AI and run an analysis. See [Generate code resolutions in Agent mode](#generate-code-resolutions-in-agent-mode).
3. To use the Solution Server:
   - Connect to the MTA Hub and run an analysis using a profile downloaded from the Hub.
   - Apply code resolutions suggested by the Solution Server. See [Apply resolutions from the Solution Server](#apply-resolutions-from-the-solution-server).

### Configure the model secret key

*JTBD Statement: "When I am setting up the environment to enable the Solution Server, I want to configure a Kubernetes secret for my LLM provider in the OpenShift project, so that Red Hat Developer Lightspeed for MTA can securely access the Large Language Model and create the necessary backend resources."*

You must configure the Kubernetes secret for the LLM provider in the Red Hat OpenShift project where you installed the MTA Operator.

> **Note:** You can replace `oc` in the following commands with `kubectl`. You can also set the base URL as the `kai_llm_baseurl` variable in the Tackle CR.

**Procedure**

Create a credentials secret named `kai-api-keys` in the `openshift-mta` project. Use the command for your provider:

> **Note:** If you do not configure the LLM API key secret, Red Hat Developer Lightspeed for MTA does not create the resources necessary to run the Solution Server.

**For Amazon Bedrock:**
```bash
oc create secret generic aws-credentials \
  --from-literal AWS_ACCESS_KEY_ID=<YOUR_AWS_ACCESS_KEY_ID> \
  --from-literal AWS_SECRET_ACCESS_KEY=<YOUR_AWS_SECRET_ACCESS_KEY>
```

**For Azure OpenAI:**
```bash
oc create secret generic kai-api-keys -n openshift-mta \
  --from-literal AZURE_OPENAI_API_KEY='<YOUR_AZURE_OPENAI_API_KEY>'
```

**For Google:**
```bash
oc create secret generic kai-api-keys -n openshift-mta \
  --from-literal GEMINI_API_KEY='<YOUR_GOOGLE_API_KEY>'
```

**For OpenAI-compatible providers:**
```bash
oc create secret generic kai-api-keys -n openshift-mta \
  --from-literal OPENAI_API_BASE='https://example.openai.com/v1' \
  --from-literal OPENAI_API_KEY='<YOUR_OPENAI_API_KEY>'
```

Optionally, force a reconcile so the MTA Operator picks up the secret immediately:
```bash
kubectl patch tackle tackle -n openshift-mta --type=merge \
  -p '{"metadata":{"annotations":{"konveyor.io/force-reconcile":"true"}}}'
```

### Enable LLM proxy in the Tackle custom resource

*JTBD Statement: "When I am configuring the migration environment on OpenShift, I want to enable the LLM proxy and Solution Server in the Tackle custom resource, so that I can provide a secure, centralized connection to the LLM and activate the shared memory of code resolutions for my team."*

To use the LLM proxy service, you must enable the proxy in the Tackle custom resource (CR) and deploy it in the Red Hat OpenShift project where you installed the MTA Operator. The proxy authenticates to the LLM using the cluster secret configured by the Administrator.

To use the Solution Server, enable it in the Tackle CR along with the proxy service. You cannot use the Solution Server without the proxy service.

**Prerequisites**

- You deployed an additional RWO volume for the Red Hat Developer Lightspeed for MTA database if you want to use the Solution Server.
- You installed the MTA Operator v8.1.0 or later.

**Procedure**

1. Log in to the Red Hat OpenShift cluster and switch to the `openshift-mta` project.
2. Create the Tackle CR in the `tackle_hub.yaml` file:
   ```bash
   vi tackle_hub.yaml
   ```
3. Enable `kai_llm_proxy_enabled` in the Tackle CR:

   ```yaml
   ---
   kind: Tackle
   apiVersion: tackle.konveyor.io/v1alpha1
   metadata:
     name: mta
     namespace: openshift-mta
   spec:
     kai_llm_proxy_enabled: true
     kai_solution_server_enabled: true
     kai_llm_provider: <provider-name>  # For example, OpenAI
     kai_llm_model: <model-name>
   ---
   ```

4. Save the Tackle CR configuration.
5. Apply the Tackle CR in the `openshift-mta` project:
   ```bash
   oc apply -f tackle_hub.yaml
   ```
6. Verify the Red Hat Developer Lightspeed for MTA resources deployed for the Solution Server:
   ```bash
   oc get deploy,svc -n openshift-mta | grep -E 'kai-(api|db|importer)'
   ```

When you enable the Solution Server, the Solution Server API endpoint is served through the MTA Hub. No additional tasks — such as creating a route for the Solution Server API — are required.

### Configure LLM provider settings

*JTBD Statement: "When I am setting up the MTA extension to use a specific AI engine, I want to configure the provider-settings.yaml file with the correct environment variables and model arguments, so that the extension can successfully communicate with my chosen LLM to generate code resolutions."*

Red Hat Developer Lightspeed for MTA is LLM-agnostic and integrates with an LLM of your choice. To enable the extension to use your chosen LLM, you must configure the `provider-settings.yaml` file.

The `provider-settings.yaml` file contains a list of LLM providers supported by default. The required environment variables differ for each provider. Access the file from the Visual Studio Code Command Palette by typing **Open the GenAI model provider configuration file**.

> **Note:** Select one provider by placing the `&active` YAML anchor on that provider's name. To switch providers, move the `&active` anchor to a different provider block.

**OpenShift AI — hosted model**

For a model named `my-model` deployed in OpenShift AI with `example-model` as the serving name:

```yaml
models:
  openshift-example-model: &active
    environment:
      CA_BUNDLE: "<Server's CA Bundle path>"
    provider: "ChatOpenAI"
    args:
      model: "my-model"
      configuration:
        baseURL: "https://<serving-name>-<data-science-project-name>.apps.konveyor-ai.example.com/v1"
```

> **Note:** When you change the model deployed in OpenShift AI, you must also update the `model` argument and the `baseURL` endpoint.

**OpenAI**

```yaml
OpenAI: &active
  environment:
    OPENAI_API_KEY: "<your-API-key>"  # Required
  provider: ChatOpenAI
  args:
    model: gpt-4o  # Required
```

**Azure OpenAI**

```yaml
AzureChatOpenAI: &active
  environment:
    AZURE_OPENAI_API_KEY: ""  # Required
  provider: AzureChatOpenAI
  args:
    azureOpenAIApiDeploymentName: ""  # Required
    azureOpenAIApiVersion: ""         # Required
```

**Amazon Bedrock**

```yaml
AmazonBedrock: &active
  environment:
    AWS_ACCESS_KEY_ID: ""      # Required if ~/.aws/credentials is not present
    AWS_SECRET_ACCESS_KEY: ""  # Required if ~/.aws/credentials is not present
    AWS_DEFAULT_REGION: ""     # Required
  provider: ChatBedrock
  args:
    model: meta.llama3-70b-instruct-v1:0  # Required
```

> **Note:** Verify command-line access to AWS services using the AWS CLI before configuring the provider settings.

**Google Gemini**

```yaml
GoogleGenAI: &active
  environment:
    GOOGLE_API_KEY: ""  # Required
  provider: ChatGoogleGenerativeAI
  args:
    model: gemini-2.5-pro  # Required
```

**Ollama — local model**

```yaml
models:
  ChatOllama: &active
    provider: "ChatOllama"
    args:
      model: "granite-code:8b-instruct"
      baseUrl: "127.0.0.1:11434"
```

### Deploy an LLM as a service in an OpenShift AI cluster

*JTBD Statement: "When I need high-performance, specialized code suggestions for specific migration targets, I want to deploy an LLM as a service on the OpenShift AI platform, so that I can run optimized models within my own scalable and secure infrastructure."*

The code suggestions from Red Hat Developer Lightspeed for MTA differ based on the LLM you use. You might want to use an LLM that can perform well on code fix tasks for your specific migration target.

An example workflow to configure an LLM service on OpenShift AI requires the following configurations:

**Configure infrastructure resources:**
1. Provision a Red Hat OpenShift cluster and install the OpenShift AI Operator.
2. Configure a GPU machineset.
3. (Optional) Configure an auto scaler CR and a machine scaler CR.

**Configure the OpenShift AI platform:**
1. Configure a data science project.
2. Configure a serving runtime.
3. Configure an accelerator profile.

**Deploy the LLM through OpenShift AI:**
1. Upload your model to an AWS-compatible bucket.
2. Add a data connection.
3. Deploy the LLM in your OpenShift AI data science project.
4. Export the SSL certificate, `OPENAI_API_BASE` URL, and other environment variables to access the LLM.

**Prepare the LLM for analysis:**
1. Configure an OpenAI API key.
2. Update the OpenAI API key and base URL in the `provider-settings.yaml` file. See [Configure LLM provider settings](#configure-llm-provider-settings).

### Configure an LLM locally in Podman Desktop

*JTBD Statement: "When I want to run a local development environment without external model dependencies, I want to configure an open-source model using Podman AI Lab, so that I can test AI-assisted code resolutions directly on my workstation."*

The Podman AI Lab extension enables you to use an open source model from a curated list and run it locally on your system.

**Prerequisites**

- You installed Podman Desktop.
- You completed the initial configurations in Red Hat Developer Lightspeed for MTA required for analysis.

**Procedure**

1. Go to the Podman AI Lab extension and click **Catalog** under **Models**.
2. Download one or more models.
3. Go to **Services** and click **New Model Service**.
4. Select a downloaded model from the **Model** drop-down menu and click **Create Service**.
5. Click the deployed model service to open the **Service Details** page.
6. Note the server URL and the model name. You must configure these in the Red Hat Developer Lightspeed for MTA extension.
7. Export the inference server URL:
   ```bash
   export OPENAI_API_BASE=<server-url>
   ```
8. In the Red Hat Developer Lightspeed for MTA extension, type **Open the GenAI model provider configuration file** in the Command Palette to open the `provider-settings.yaml` file.
9. Enter the model details from Podman Desktop. For example, for a Mistral model:

   ```yaml
   podman_mistral: &active
     provider: "ChatOpenAI"
     environment:
       OPENAI_API_KEY: "unused value"
     args:
       model: "ibm-granite/granite-3.3-8b-instruct-GGUF"
       configuration:
         baseURL: "http://localhost:56885/v1"
   ```

   > **Note:** The Podman Desktop service endpoint does not require a password, but the OpenAI library expects `OPENAI_API_KEY` to be set. In this case, the value does not matter.

> **Warning:** Models deployed through the Podman AI Lab were found to be insufficient for the complexity of code changes required to fix issues discovered by MTA. Do not use such models in a production environment.

### Configure IDE settings

*JTBD Statement: "When I have installed the MTA extension in Visual Studio Code, I want to provide my LLM credentials and configure the extension settings, so that I can activate Red Hat Developer Lightspeed for MTA and prepare the IDE for AI-assisted code resolutions."*

After you install the MTA extension in Visual Studio Code, provide your LLM credentials to activate Red Hat Developer Lightspeed for MTA settings.

**Prerequisites**

- You completed the Solution Server configurations in the Tackle CR if you want to use the Solution Server.

**Procedure**

1. Go to the Red Hat Developer Lightspeed for MTA settings in one of the following ways:
   - Click **Extensions > MTA Extension for Visual Studio Code > Settings**.
   - Type **Ctrl+Shift+P** or **Cmd+Shift+P** to open the Command Palette and enter **Preferences: Open Settings (UI)**. Go to **Extensions > MTA** to open the settings page.
2. Configure the required extension settings.

For a full list of available settings and their descriptions, see [IDE extension settings](#ide-extension-settings) in the Reference section.

### Configure analysis profile settings

*JTBD Statement: "When I am preparing to analyze a Java project for modernization, I want to define my target technologies and rule sets in an analysis profile, so that the extension identifies the correct issues and generates relevant AI-assisted code fixes tailored to my project."*

You can use the MTA Visual Studio Code extension to run an analysis and discover issues in the code. You can optionally enable Red Hat Developer Lightspeed for MTA to get AI-assisted code fix suggestions for the identified issues.

**Prerequisites**

- You completed the Solution Server configurations in the Tackle CR if you want to use the Solution Server.
- You opened a Java project in your Visual Studio Code workspace.

**Procedure**

1. Open the **MTA View Analysis** page in either of the following ways:
   - Click the book icon on the **MTA: Issues** pane of the MTA extension.
   - Type **Ctrl+Shift+P** or **Cmd+Shift+P** to open the Command Palette and enter **MTA: Open Analysis View**.
2. Click the settings button on the **MTA View Analysis** page to configure a profile for your project. The **Get Ready to Analyze** pane lists the basic configurations required for an analysis.

For a full list of profile parameters, see [Profile configuration settings](#profile-configuration-settings) in the Reference section.

**Verification**

After completing the profile configuration, close the **Get Ready to Analyze** pane and run an analysis to verify that your configuration works.

---

## Migrate

*JTBD Statement: "When I am refactoring complex Java codebases, I want to apply AI-generated resolutions and iterate through code fixes, so that I can modernize my applications with minimum manual effort."*

After completing configuration, run an analysis to identify issues in the code and generate suggestions to resolve them. You can get fix suggestions in two ways: Solution Server mode and Agent AI mode.

When you run an analysis, MTA displays the issues in the **Analysis Results** view. When you request code fix suggestions, Red Hat Developer Lightspeed for MTA:

- Streams LLM messages describing the issue, the resolution, and the file to be updated.
- Generates new files in the **Resolutions** pane with the updated code.
- Allows you to review, apply, or revert the changes.

If you apply all resolutions, Red Hat Developer Lightspeed for MTA applies the changes and triggers another analysis to check for remaining issues. Later analyses report fewer issues as the codebase converges on the migration target.

### Apply resolutions from the Solution Server

*JTBD Statement: "When I am reviewing identified migration issues, I want to use success metrics and confidence levels derived from real-world usage data, so that I can apply verified code resolutions from the Solution Server with high confidence and minimal risk."*

When you request code resolutions using the Solution Server, an issue displays a success metric when one becomes available. A success metric indicates the confidence level in applying the code fix based on real-world usage data from previous analyses.

**Prerequisites**

- You opened a Java project in your Visual Studio Code workspace.
- You configured a profile on the **MTA Analysis View** page.
- You ran an analysis after enabling the Solution Server.

**Procedure**

1. Review the issues from the **Analysis results** space of the **MTA View Analysis** page. Use the following tabs:
   - **All:** Lists all incidents identified in your project.
   - **Files:** Lists all files for which the analysis identified issues.
   - **Issues:** Lists all issues across different files.
2. Use the **Category** drop-down to filter issues by how critical the fix is for the target migration: mandatory, potential, or optional.
3. Click **Has Success Rate** to see how many times the same issue resolution was accepted in previous analyses.
4. Click the solution icon to trigger automated updates to your code. If you applied a filter, code updates are made only for the filtered incidents, files, or issues.
5. Review and optionally edit the code.
6. Click **Apply all** in the **Resolutions** pane to permanently apply the changes.

### Generate code resolutions in Agent mode

*JTBD Statement: "When I want an autonomous AI agent to resolve migration issues in my code, I want to use Agent mode to automatically plan, execute, and iteratively fix both base code and diagnostic issues, so that I can reach a fully modernized state with minimal manual intervention."*

In Agent mode, the Red Hat Developer Lightspeed for MTA planning agent creates the context for an issue and picks a sub-agent suited to resolve it. The sub-agent runs an automated analysis and displays the reasoning transcript alongside the files to be changed.

The agent runs another automated analysis to detect new issues that may have occurred because of the accepted changes or diagnostic issues generated by your toolchain after a previous change. It continues until all issues are resolved or it has made a maximum of two attempts to fix any single issue.

> **Note:** During an Agent AI stream, you can reject changes or stop the stream, but you cannot edit the updated files while the stream is in progress. The agent generates a new preview in each iteration; the time taken depends on the number of new diagnostic issues detected.

**Prerequisites**

- You opened a Java project in your Visual Studio Code workspace.
- You configured an analysis profile on the **MTA Analysis View** page.

**Procedure**

1. Verify that Agent mode is enabled in one of the following ways:
   - Type **Ctrl+Shift+P** (Linux/Windows) or **Cmd+Shift+P** (Mac) to open the Command Palette. Enter **Preferences: Open User Settings (JSON)** to open `settings.json`. Ensure that `mta-vscode-extension.genai.agentMode` is set to `true`.
   - Go to **Extensions > Red Hat Developer Lightspeed for MTA > Settings** and click **Agent Mode** to enable it.
2. Click the Red Hat Developer Lightspeed for MTA extension and click **Open MTA Analysis View**.
3. Select a profile for the analysis.
4. Click **Start** to start the MTA RPC server.
5. Click **Run Analysis** on the **MTA Analysis View** page. The **Resolution Details** tab opens, where you can view the automated analysis and the files to be changed.
6. Click **Review Changes** to open the editor in diff view for the modified file.
7. Review the changes and click **Apply** to update the file with all changes, or **Reject** to reject all changes. If you apply the changes, Red Hat Developer Lightspeed for MTA creates the updated file.
8. Open **Source Control** to access the updated file.
9. In the **Resolution Details** view, accept the proposal from Red Hat Developer Lightspeed for MTA to make further changes. The analysis repeats, after which you can review and accept the changes until all issues are resolved.

---

## Troubleshoot

*JTBD Statement: "When I encounter errors in the extension or LLM communication, I want to access and archive diagnostic logs, so that I can fix the problem and resume my migration work."*

Red Hat Developer Lightspeed for MTA generates logs to debug issues specific to the extension host and the MTA analysis and RPC server. You can also configure the log level to control the verbosity of logging.

- **Extension logs** are stored as `extension.log` with automatic rotation. The maximum size of the log file is 10 MB and three files are retained.
- **Analyzer RPC logs** are stored as `analyzer.log` without rotation.

### Access the logs

*JTBD Statement: "When I am investigating unexpected behavior or errors within the extension, I want to access the raw logs from the extension host, the analyzer server, and the webview interface, so that I can pinpoint the root cause of the issue."*

You can access the logs in the following ways:

- **Log file:** Type **Developer: Open Extension Logs Folder** in the Command Palette and open the `redhat.mta-vscode-extension` directory, which contains both the extension log and the analyzer log.
- **Output panel:** Select **Red Hat Developer Lightspeed for MTA** from the drop-down menu in the **Output** panel.
- **Webview logs:** Type **Open Webview Developer Tools** in the Command Palette to inspect webview content.

### Archive the logs

*JTBD Statement: "When I encounter technical issues with the extension, I want to generate a consolidated zip archive of logs and configurations, so that I can provide support teams with the diagnostic data needed for resolution while maintaining security."*

To archive the logs as a zip file, type **MTA: Generate Debug Archive** in the Visual Studio Code Command Palette and select the information type to include.

The archive command captures all relevant log files in a zip archive at the specified location in your project. By default, the archived logs are stored in the `.vscode` directory of your project.

The archive can include the following information:

- **LLM provider configuration:** Fields from the provider settings. All fields are redacted for security reasons by default. Do not enable unredacted archiving unless you are certain no sensitive information is included.
- **LLM model arguments:** Arguments specified for your model.
- **LLM traces:** If you enabled tracing LLM interactions, you can choose to include LLM traces in the archive.

---

## Reference

*JTBD Statement: "When I am setting up or automating my environment, I want to look up exact technical parameters and supported model values, so that I can configure the system accurately."*

### Configurable Large Language Models and providers

*JTBD Statement: "When I am configuring the LLM provider in the Tackle custom resource, I want to identify the correct provider keys and compatible models, so that I can successfully connect the MTA extension to my chosen AI service."*

The following table lists the LLM providers and example models that can be configured in the Tackle custom resource (CR).

| LLM provider | Tackle CR value | Example models |
|--------------|-----------------|----------------|
| OpenShift AI platform | — | Models deployed in an OpenShift AI cluster accessible via OpenAI-compatible API |
| OpenAI | `openai` | `gpt-4`, `gpt-4o`, `gpt-4o-mini`, `gpt-3.5-turbo` |
| Azure OpenAI | `azure_openai` | `gpt-4`, `gpt-35-turbo` |
| Amazon Bedrock | `bedrock` | `anthropic.claude-3-5-sonnet-20241022-v2:0`, `meta.llama3-1-70b-instruct-v1:0` |
| Google Gemini | `google` | `gemini-2.0-flash-exp`, `gemini-1.5-pro` |
| Ollama | `ollama` | `llama3.1`, `codellama`, `mistral` |

The availability of public LLM models is maintained by the respective LLM provider.

### IDE extension settings

*JTBD Statement: "When I am fine-tuning my modernization environment, I want to configure the extension settings, so that I can control AI behavior, logging levels, and storage paths to suit my specific development workflow."*

The following settings can be configured for the Red Hat Developer Lightspeed for MTA extension in Visual Studio Code.

| Setting | Description |
|---------|-------------|
| **Log level** | Sets the verbosity of logs for the MTA binary. The default level is `debug`. |
| **Analyzer path** | Specifies a custom path to the MTA binary. If blank, the default path is used. |
| **Auto Accept on Save** | Enabled by default. Saves updated code automatically in a new file when a suggested change is accepted. Disable to manually save changes. |
| **Gen AI: Enabled** | Enabled by default. Enables AI-assisted code fixes through Red Hat Developer Lightspeed for MTA. |
| **Gen AI: Agent mode** | Activates the experimental Agent AI flow for automated file analysis and resolution. |
| **Gen AI: Excluded diagnostic sources** | Lists diagnostic sources to exclude from the automated Agent AI analysis. Configured in `settings.json`. |
| **Cache directory** | The file system path where cached LLM responses are stored. |
| **Trace directory** | The absolute path to the directory that contains saved LLM interaction traces. |
| **Trace enabled** | Enables tracing of MTA communication with the LLM. Traces are saved to the configured trace directory. |
| **Demo mode** | Runs the extension using cached LLM responses instead of live queries. |
| **Debug: Webview** | Enables debug-level logging for Webview message handling in Visual Studio Code. |

### Profile configuration settings

*JTBD Statement: "When I am preparing to analyze an application, I want to define specific labels, rules, and AI providers in an analysis profile, so that the LLM receives the precise technical context required to generate relevant code fixes."*

The following profile settings define the context before you request a code fix for a particular application.

| Setting | Description |
|---------|-------------|
| **Select profile** | Creates a reusable set of analysis configurations. The profile name is part of the context given to the LLM. |
| **Configure label selector** | Filters rules for analysis based on source or target technology. Specify one or more technologies, for example, `cloud-readiness` or `quarkus`. You must configure either a target or source technology before running an analysis. If you defined a new target or source technology in a custom rule, type its name to add it to the list. Red Hat provides over 2,400 default rules. |
| **Set rules** | Enables default rules and lets you select custom rules for the analysis. |
| **Configure generative AI** | Opens the `provider-settings.yaml` file containing API keys and model arguments for all supported LLMs. |

### Project terminology

*JTBD Statement: "When I am discussing modernization strategies or reviewing tool outputs, I want to understand the specific terminology used by Red Hat Developer Lightspeed for MTA, so that I can accurately interpret system performance and collaborate effectively with my team."*

| Term | Definition |
|------|------------|
| **Migration hint** | A pattern of resolution extracted by the Solution Server to help the LLM generate more accurate fixes in future analyses. |
| **Solved example** | A code change from a previous migration stored in the Solution Server. Solved examples build a collective organizational memory that improves fix accuracy over time. |
| **Success metric** | A confidence level derived from real-world usage data indicating the likelihood that a code fix is correct for a given issue. |
| **Context** | The combination of source code, issue descriptions, and solved examples given to the LLM to generate a fix suggestion. |
| **RPC server** | The analyzer Remote Procedure Call (RPC) server that runs the MTA analysis engine inside Visual Studio Code. |
| **RWO volume** | A ReadWriteOnce (RWO) persistent volume. The Solution Server database requires a 5Gi RWO persistent volume. |
