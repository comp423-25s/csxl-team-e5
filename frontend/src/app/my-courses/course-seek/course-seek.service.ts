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

  async chat(input: string) {
    return this.http.post<ChatResourceResponse>(`/api/academics/chat`, {
      input
    });
  }
}
