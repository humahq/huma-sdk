## Instructions for Running Test Cases

To execute the test cases, follow these steps:

1. Set the required environment variables:

   ```bash
   export API_URL=<insert your API URL>
   export API_SECRET_KEY=<insert your API token>
   ```

   Replace `<insert your API URL>` and `<insert your API token>` with the appropriate values for your environment.

2. In the `nose2.cfg` file, configure the `code_directories` to specify which test cases to run. You can specify either the 'integration' or 'unit' directory to run tests specific to integration or unit testing, or include both if you want to run all available test cases.

   For example, if you want to run only unit tests, set the `code_directories` as follows:

   ```
   code_directories = unit
   ```

   If you want to run both integration and unit tests, use:

   ```
   code_directories = integration
                      unit
   ```

3. Run the following command to execute the test cases:

   ```bash
   nose2 -v
   ```

   The `-v` flag is used for verbose mode to display detailed information about the test execution.

**Note** :- Before running the test cases, ensure you are in the root folder of the project.