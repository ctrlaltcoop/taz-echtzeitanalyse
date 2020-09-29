export const REFERRER_LABEL_ANDERE_KLEINE = 'Andere kleine Referrer'
export const REFERRER_LABEL_TAZ = 'taz'
export const REFERRER_LABEL_FACEBOOK = 'Facebook'
export const REFERRER_LABEL_TWITTER = 'Twitter'
export const REFERRER_LABEL_INSTAGRAM = 'Instagram'
export const REFERRER_LABEL_TELEGRAM = 'Telegram'
export const REFERRER_LABEL_GOOGLE = 'Google'
export const REFERRER_LABEL_UPDAY = 'Upday'
export const REFERRER_LABEL_BING = 'Bing'
export const REFERRER_LABEL_ECOSIA = 'Ecosia'
export const REFERRER_LABEL_DUCKDUCKGO = 'DuckDuckGo'
export const REFERRER_LABEL_T_ONLINE = 'T-Online'
export const REFERRER_LABEL_WEB_DE = 'Web.de'
export const REFERRER_LABEL_YAHOO = 'Yahoo'
export const REFERRER_LABEL_NEWSTRAL = 'Newstral'
export const REFERRER_LABEL_WIKIPEDIA = 'Wikipedia'
export const REFERRER_LABEL_FLIPBOARD = 'Flipboard'
export const REFERRER_LABEL_POCKET = 'Pocket'
export const REFERRER_LABEL_UNBEKANNT = 'Unbekannt'
export const DEVICE_LABEL_DESKTOP = 'Desktop'
export const DEVICE_LABEL_MOBILE = 'Mobil'
export const DEVICE_LABEL_UNCLASSIFIED = 'unclassified'

// Those labels should not be used anymore and can be removed in the future
export const DEVICE_LABEL_DESKTOP_DEPRECATED = 'desktop'
export const DEVICE_LABEL_MOBILE_DEPRECATED = 'mobile'
export const DEVICE_LABEL_MASTODON_DEPRECATED = 'mastodonpod'

export const referrerColors: {[key: string]: string} = {
  [REFERRER_LABEL_ANDERE_KLEINE]: '#272727',
  [REFERRER_LABEL_TAZ]: '#d50d2e',
  [REFERRER_LABEL_FACEBOOK]: '#4e69a2',
  [REFERRER_LABEL_TWITTER]: '#1da1f2',
  [REFERRER_LABEL_INSTAGRAM]: '#D200B3',
  [REFERRER_LABEL_TELEGRAM]: '#3F4A57',
  [REFERRER_LABEL_GOOGLE]: '#00A661',
  [REFERRER_LABEL_UPDAY]: '#7EB7DB',
  [REFERRER_LABEL_BING]: '#008875',
  [REFERRER_LABEL_ECOSIA]: '#CDE31B',
  [REFERRER_LABEL_DUCKDUCKGO]: '#E7572C',
  [REFERRER_LABEL_T_ONLINE]: '#F7008A',
  [REFERRER_LABEL_WEB_DE]: '#FFDD00',
  [REFERRER_LABEL_YAHOO]: '#6302de',
  [REFERRER_LABEL_NEWSTRAL]: '#F6F6F6',
  [REFERRER_LABEL_WIKIPEDIA]: '#6B6B6B',
  [REFERRER_LABEL_FLIPBOARD]: '#FFBCC1',
  [REFERRER_LABEL_POCKET]: '#FF7B99',
  [REFERRER_LABEL_UNBEKANNT]: '#C6C6C6'
}

export const deviceColors: {[key: string]: string} = {
  [DEVICE_LABEL_DESKTOP_DEPRECATED]: '#6302de',
  [DEVICE_LABEL_DESKTOP]: '#6302de',
  [DEVICE_LABEL_MOBILE_DEPRECATED]: '#ff9900',
  [DEVICE_LABEL_MOBILE]: '#ff9900',
  [DEVICE_LABEL_MASTODON_DEPRECATED]: '#ff9900',
  [DEVICE_LABEL_UNCLASSIFIED]: '#C6C6C6'
}
