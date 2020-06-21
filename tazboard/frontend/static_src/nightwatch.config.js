module.exports = {
  "test_settings": {
    "chrome": {
      "webdriver": {
        "server_path": process.env.CHROMEDRIVER_BIN || require('chromedriver').path
      },
      "desiredCapabilities": {
        "browserName": "chrome",
        "chromeOptions": {
          "args": [
            "--headless",
            "--no-sandbox",
            "--disable-gpu"
          ]
        }
      }
    },
    "firefox": {
      "webdriver": {
        "server_path": require('geckodriver').path
      },
      "desiredCapabilities": {
        "browserName": "firefox",
        "alwaysMatch": {
            "moz:firefoxOptions": {
                "args": [ "-headless" ]
            }
        }
      }
    }
  }
}
