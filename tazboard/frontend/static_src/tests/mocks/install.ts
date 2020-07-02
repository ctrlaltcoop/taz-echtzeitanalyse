import fetchMock from 'fetch-mock'
import histogram24h from './histogram-24h.json'
import referrer24h from './referrer-24h.json'

fetchMock.mock('/api/v1/histogram', {
  status: 200,
  body: histogram24h
}, {
  query: {
    min: 'now-24h'
  }
})

fetchMock.mock('/api/v1/referrer', {
  status: 200,
  body: referrer24h
}, {
  query: {
    min: 'now-24h'
  }
})
