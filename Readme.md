1. **Create the Aptfile**:
   - In the root of your local project directory (the same directory where your `requirements.txt` and other project files are located), create a file named `Aptfile`.
   - Inside this file, add the line `libgl1-mesa-glx` to specify that Heroku should install the `libGL` library. Your `Aptfile` should look like this:
     ```
     libgl1-mesa-glx
     ```

2. **Update the Buildpacks**:
   - If you haven’t already added the Heroku Apt buildpack to your app, do so by running the following command in your terminal:
     ```bash
     heroku buildpacks:add --index 1 heroku-community/apt -a your-app-name
     ```
     Replace `your-app-name` with the actual name of your Heroku app.
   - Ensure that the Python buildpack is also added since your application is a Python app. You can verify your buildpacks with:
     ```bash
     heroku buildpacks -a your-app-name
     ```
   - The buildpacks should include both `heroku/python` and `heroku-community/apt`.

3. **Test Locally** (Optional):
   - While you can't directly test the Apt buildpack locally, you can ensure that the rest of your application is functioning as expected.
   - Run your application locally to make sure there are no other issues. If you're using FastAPI with Uvicorn, you can typically run it using a command like:
     ```bash
     uvicorn your_app_module:app --reload
     ```

4. **Commit and Push Changes**:
   - Once you're ready, commit the `Aptfile` to your Git repository:
     ```bash
     git add Aptfile
     git commit -m "Add Aptfile to install libGL on Heroku"
     ```
   - Push the changes to your Heroku app:
     ```bash
     git push heroku master
     ```

5. **Redeploy on Heroku**:
   - After pushing the changes, Heroku will automatically trigger a new build and deploy process.
   - Monitor the build logs in the Heroku dashboard to ensure that the `libgl1-mesa-glx` package is installed without errors.
   