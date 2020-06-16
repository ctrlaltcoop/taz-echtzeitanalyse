/**
 * A Nightwatch page object. The page object name is the filename.
 *
 * Example usage:
 *   browser.page.homepage.navigate()
 *
 * For more information on working with page objects see:
 *   https://nightwatchjs.org/guide/working-with-page-objects/
 *
 */

module.exports = {
  url: '/static/app',
  commands: [],

  elements: {
    appContainer: '#app'
  },
  sections: {
    app: {
      selector: '#app',
      elements: {
        timeframeCaption: {
          selector: 'span.timeframe-caption'
        },
        timeframeSelect: {
          selector: 'select.timeframe-select'
        }
      }
    }
  }
}
