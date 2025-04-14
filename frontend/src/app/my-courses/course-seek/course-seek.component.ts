import { Component, OnInit, signal, WritableSignal } from '@angular/core';
import { ChatResourceResponse, CourseSeekService } from './course-seek.service';
import { map } from 'rxjs';
import { ChatService } from 'src/app/shared/chat-service/chat-service';
import { v4 as uuidv4 } from 'uuid';

interface ChatHistory extends ChatResourceResponse {
  role: 'assistant' | 'user';
}

@Component({
  selector: 'app-course-seek',
  templateUrl: './course-seek.component.html',
  styleUrl: './course-seek.component.css'
})
export class CourseSeekComponent implements OnInit {
  text_input: WritableSignal<string> = signal('');
  chat_history: WritableSignal<ChatHistory[]> = signal([]);
  default_msg: WritableSignal<ChatHistory> = signal({
    role: 'assistant',
    message: 'Hi, I am CourseSeek. How can I help you today?',
    sections: null
  });

  public sessionId: string =
    sessionStorage.getItem('chat_session_id') || uuidv4();

  constructor(
    private resourceService: CourseSeekService,
    protected chatService: ChatService
  ) {}

  ngOnInit(): void {
    sessionStorage.setItem('chat_session_id', this.sessionId);
    this.loadChatHistory();
  }

  loadChatHistory() {
    this.resourceService.getChatHistory(this.sessionId).subscribe({
      next: (history: ChatHistory[]) => {
        this.chat_history.set(history);
      },
      error: (error) => {
        console.error('Error loading chat history: ', error);
      }
    });
  }

  async getChatCompletions(user_input: string) {
    const courseSeekResponse = await this.resourceService.chat(
      user_input,
      this.sessionId
    );
    const toChatHistory = (response: ChatResourceResponse, role: string) => {
      return {
        ...response,
        role: role as 'assistant' | 'user'
      } as ChatHistory;
    };

    this.chat_history.set([
      ...this.chat_history(),
      toChatHistory({ sections: null, message: user_input }, 'user')
    ]);

    courseSeekResponse
      .pipe(
        map((response) =>
          this.chat_history.set([
            ...this.chat_history(),
            toChatHistory(response, 'assistant')
          ])
        )
      )
      .subscribe();

    this.text_input.set('');
  }

  toggleChatWindow() {
    this.chatService.toggleChatWindow();
  }
}
