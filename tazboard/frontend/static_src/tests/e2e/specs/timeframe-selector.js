/// /////////////////////////////////////////////////////////////
// For authoring Nightwatch tests, see
// https://nightwatchjs.org/guide
//
// For more information on working with page objects see:
//   https://nightwatchjs.org/guide/working-with-page-objects/
/// /////////////////////////////////////////////////////////////

module.exports = {
  beforeEach: (browser) => browser.init(),

  'verify correct timeframe is displayed when chaning selector': (browser) => {
    const dashboard = browser.page.dashboard()
    const app = dashboard.section.app
    dashboard.waitForElementVisible('@appContainer')
    app.click('@timeframeSelect', () => {
      app.click("option[value='1_DAY']")
    })
    browser.assert.urlContains('timeframeId=1_DAY')
    browser.end()
  }
}
