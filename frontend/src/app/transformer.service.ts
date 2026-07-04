import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { BotInfo, TransformRequest, TransformResponse } from './transformer.model';

@Injectable({ providedIn: 'root' })
export class TransformerService {
  constructor(private http: HttpClient) {}

  listBots(): Observable<BotInfo[]> {
    return this.http.get<BotInfo[]>('/api/bots');
  }

  transform(request: TransformRequest): Observable<TransformResponse> {
    return this.http.post<TransformResponse>('/api/transform', request);
  }
}
