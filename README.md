# RaidenNLLB

**RaidenNLLB** is a powerful Python plugin that brings multilingual translation directly into your Word documents. Built on the *facebook/nllb-200-1.3B* model, it supports over 200 languages with high-quality translations. The plugin also offers flexible configuration options, allowing users to tailor translation behavior to their specific needs.

## Requirements

- **Python 3.x** – Ensure Python is installed on your system.
- **office add-in debugging tools** - Ensure Office add-in debugging tools is installed on your system.
- **Yeoman and generator-office** - Ensure Yeoman and generator-office is installed on your system.
- **Node.js** - Ensure Node.js is installed on your system.

## How to Run

1. **Clone the Repository**  
   Clone or download this repository to your local machine.

2. **Navigate to the Project Directory and run Add-in Office**  
   Open your terminal or command prompt and change to the project directory (folder RaidenEi). 
   Execute the following command:
   ```bash
   npm start

3. **Run the Python File**  
   Execute the following command:
   ```bash
   python trans.py

4. In case the node_modules folder is missing
   Execute the following command:
   ```bash
   npm install
   This command will use the package.json file to download the required packages such as webpack, webpack-cli, node-fetch, etc.

5. In case "Unable to start the dev server. Error: The dev server is not running on port 3000."
   Execute the following command:
   ```bash
   npx webpack --config webpack.config.js
   This command runs Webpack using the specified configuration file webpack.config.js.

5. In case "Error: Cannot find module 'webpack-cli/package.json'"
   Execute the following command:
   ```bash
   npm install --save-dev webpack webpack-cli
   This command installs webpack and webpack-cli as development dependencies in your project.
   

## Notice: You have to notice those condition below to make sure application runs:

**1.** When run file if you facing error you should open full folder in you IDE for making sure file reading is success
   Folder structure in your IDE should be like this:
         EX2
         |---RaidenEi
             |--- (other files)
         |---README.md
         |---Model
             |--- trans.py

**2.** You have to trust (in case the window pop up to asking for trusting the source) or else it won't run.

**3.** In case the facebook/nllb-200-1.3B model is too large (around 5.84GB) or if any installation issues arise that could affect the evaluation process, I have recorded a demo showcasing the implemented features to facilitate the assessment by the instructors. 
Link: https://youtu.be/sCFfCvbbRyY

## Output

When successfully executed, the plugin integrates into your Word workplace, supporting translation tasks with added features such as:
  - Translation Customization:
       Customize translation parameters to suit your workflow.
  - Seamless Integration:
       The plugin works within your word processing environment to provide real-time translations.

