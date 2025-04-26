import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { CourseSeekCourse } from './models';
import { CourseSeekCourseCard } from './course-seek.component';

export interface ChatResourceResponse {
  courses: CourseSeekCourse[] | null;
  message: string;
}
export interface SessionResourceResponse {
  session_id: string;
  latest_message: ChatHistoryResponse;
}
export interface ChatHistoryResponse extends ChatResourceResponse {
  role: 'assistant' | 'user';
}

@Injectable({
  providedIn: 'root'
})
export class CourseSeekService {
  constructor(protected http: HttpClient) {}

  chat(input: string, sessionId: string): Observable<ChatResourceResponse> {
    return this.http.post<ChatResourceResponse>(
      `/api/academics/semantic-chat`,
      {
        session_id: sessionId,
        input
      }
    );
  }

  getChatHistory(sessionId: string): Observable<ChatHistoryResponse[]> {
    return this.http.get<ChatHistoryResponse[]>(
      `/api/academics/semantic-chat/history/${sessionId}`
    );
  }

  getChatSessions(): Observable<SessionResourceResponse[]> {
    return this.http.get<SessionResourceResponse[]>(
      "/api/academics/semantic-chat/sessions"
    )
  }
}
