import { HttpClient } from '@angular/common/http';
import { Injectable, signal, WritableSignal } from '@angular/core';
import { CatalogSection } from 'src/app/academics/academics.models';

export interface ChatResourceResponse {
  sections: CatalogSection[] | null;
  response: string;
}

@Injectable({
  providedIn: 'root'
})
export class CourseSeekService {

  constructor(protected http: HttpClient) {}

  async chat(user_input: string) {
    return await this.http.post<ChatResourceResponse>(
      `/api/academics/chat`,
      user_input
    );
  }
}
