import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { CourseSeekCourse } from './models';

export interface ChatResourceResponse {
  session_id: string;
  message: string;
  courses: CourseSeekCourse[] | null;
}

export interface ChatHistoryResponse extends ChatResourceResponse {
  role: 'assistant' | 'user';
  timestamp: string;
}

export interface SessionResourceResponse {
  session_id: string;
  latest_message: ChatHistoryResponse;
}

@Injectable({
  providedIn: 'root'
})
export class CourseSeekService {
  private readonly base = '/api/academics/semantic-chat';

  constructor(protected http: HttpClient) {}

  chat(input: string, sessionId?: string): Observable<ChatResourceResponse> {
    const sid = sessionId || sessionStorage.getItem('chat_session_id') || '';
    return this.http.post<ChatResourceResponse>(this.base, {
      session_id: sid,
      input
    });
  }

  getChatHistory(sessionId?: string): Observable<ChatHistoryResponse[]> {
    const sid = sessionId || sessionStorage.getItem('chat_session_id')!;
    return this.http.get<ChatHistoryResponse[]>(`${this.base}/history/${sid}`);
  }

  getChatSessions(): Observable<SessionResourceResponse[]> {
    return this.http.get<SessionResourceResponse[]>(`${this.base}/sessions`);
  }
}
