/* eslint @typescript-eslint/camelcase: 0 */
import { HistogramDto } from '@/dto/HistogramDto'
import { QueryParams, queryString } from '@/utils/urls'
import { ReferrerDto } from '@/dto/ReferrerDto'
import { ToplistDto } from '@/dto/ToplistDto'
import { DevicesDto } from '@/dto/DevicesDto'
import { TotalDto } from '@/dto/TotalDto'
import { SubjectsDto } from '@/dto/SubjectsDto'

export class HttpError extends Error {
  constructor (public response: Response) {
    super()
  }
}

export class BadRequest extends HttpError {
}

export class NotFound extends HttpError {
}

export class InternalServerError extends HttpError {
}

interface RequestArgs {
  signal?: AbortSignal;
}

export class ApiClient {
  baseURL = '/api/v1/'

  async total (minDate: Date, maxDate: Date, msid: number | null = null, requestArgs: RequestArgs = {}): Promise<TotalDto> {
    return await this.request<TotalDto>('total', 'GET', {
      msid,
      min_date: minDate.toISOString(),
      max_date: maxDate.toISOString()
    }, requestArgs.signal)
  }

  async histogram (minDate: Date, maxDate: Date, msid: number | null = null, subject: string | null = null, requestArgs: RequestArgs = {}): Promise<HistogramDto> {
    return await this.request<HistogramDto>('histogram', 'GET', {
      msid,
      subject,
      min_date: minDate.toISOString(),
      max_date: maxDate.toISOString()
    }, requestArgs.signal)
  }

  async referrer (minDate: Date, maxDate: Date, msid: number | null = null, requestArgs: RequestArgs = {}): Promise<ReferrerDto> {
    return await this.request<ReferrerDto>('referrer', 'GET', {
      msid,
      min_date: minDate.toISOString(),
      max_date: maxDate.toISOString()
    }, requestArgs.signal)
  }

  async toplist (minDate: Date, maxDate: Date, limit = 10, subject: string | null = null, requestArgs: RequestArgs = {}): Promise<ToplistDto> {
    return await this.request<ToplistDto>('toplist', 'GET', {
      min_date: minDate.toISOString(),
      max_date: maxDate.toISOString(),
      limit,
      subject
    }, requestArgs.signal)
  }

  async subjects (minDate: Date, maxDate: Date, limit = 10, requestArgs: RequestArgs = {}): Promise<SubjectsDto> {
    return await this.request<SubjectsDto>('subjects', 'GET', {
      min_date: minDate.toISOString(),
      max_date: maxDate.toISOString(),
      limit: limit
    }, requestArgs.signal)
  }

  async devices (minDate: Date, maxDate: Date, msgId: number | null = null, requestArgs: RequestArgs = {}): Promise<DevicesDto> {
    return await this.request<DevicesDto>('devices', 'GET', {
      msgId,
      min_date: minDate.toISOString(),
      max_date: maxDate.toISOString()
    }, requestArgs.signal)
  }

  async fireplace (minDate: Date, maxDate: Date, msid: number | null = null, requestArgs: RequestArgs = {}): Promise<ToplistDto> {
    return await this.request<ToplistDto>('fireplace', 'GET', {
      msid,
      min_date: minDate.toISOString(),
      max_date: maxDate.toISOString()
    }, requestArgs.signal)
  }

  async request<T> (path: string, method: string, queryParams: QueryParams = {}, signal: AbortSignal | null = null): Promise<T> {
    const response = await this.requestRaw(path, method, queryParams, signal)

    if (!response.ok) {
      switch (response.status) {
        case 400:
          throw new BadRequest(response)
        case 404:
          throw new NotFound(response)
        case 500:
          throw new InternalServerError(response)
        default:
          throw new HttpError(response)
      }
    }

    return (await response.json()) as T
  }

  async requestRaw (path: string, method: string, queryParams: QueryParams = {}, signal: AbortSignal | null = null): Promise<Response> {
    return fetch(this.baseURL + path + queryString(queryParams), {
      method,
      signal
    })
  }
}
