const { defineConfig } = require("cypress");
const { port, hostName } = require("./config/env/all");

module.exports = defineConfig({
    e2e: {
        baseUrl: `http://${hostName}:${port}`,
        specPattern: "test/e2e/integration/**/*.js",
        fixturesFolder: "test/e2e/fixtures",
        screenshotsFolder: "test/e2e/screenshots",
        videosFolder: "test/e2e/videos",
        supportFile: "test/e2e/support/index.js",
        video: false,
        blockHosts: "*:35729",
        setupNodeEvents(on, config) {},
    },
});
