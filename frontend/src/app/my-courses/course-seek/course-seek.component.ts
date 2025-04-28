import { Component, OnInit, signal, WritableSignal } from '@angular/core';
import {
  ChatResourceResponse,
  SessionResourceResponse,
  CourseSeekService
} from './course-seek.service';
import { ChatService } from 'src/app/shared/chat-service/chat-service';
import { MatDialog } from '@angular/material/dialog';
import { ShowCourseseekCardsComponent } from '../dialogs/show-courseseek-cards/show-courseseek-cards.component';
import { CourseSeekCourse } from './models';
import { v4 as uuidv4 } from 'uuid';


interface ChatHistory extends ChatResourceResponse {
  role: 'assistant' | 'user';
  timestamp: string;
}

@Component({
  selector: 'app-course-seek',
  templateUrl: './course-seek.component.html',
  styleUrls: ['./course-seek.component.css']
})
export class CourseSeekComponent implements OnInit {
  isMessageOpen: WritableSignal<boolean> = signal(false);
  text_input: WritableSignal<string> = signal('');
  sessions: WritableSignal<SessionResourceResponse[]> = signal([]);
  selectedSessionId: WritableSignal<string | null> = signal(null);
  chat_history: WritableSignal<ChatHistory[]> = signal([]);

  default_msg: WritableSignal<ChatHistory> = signal({
    session_id: '',
    role: 'assistant',
    message: 'Hi, I am CourseSeek. How can I help you today?',
    courses: null,
    timestamp: new Date().toISOString()
  });

  constructor(
    private resourceService: CourseSeekService,
    protected chatService: ChatService,
    private dialog: MatDialog
  ) {}

  ngOnInit(): void {
    this.loadChatSessions();

    const saved = sessionStorage.getItem('chat_session_id');
    if (saved) {
      this.selectedSessionId.set(saved);
      this.isMessageOpen.set(true);
      this.loadChatHistory(saved);
    }
  }

  startNewChat() {
    this.selectedSessionId.set(null);
    this.isMessageOpen.set(true);
    this.chat_history.set([]);
    sessionStorage.removeItem('chat_session_id');
  }

  loadChatSessions() {
    this.resourceService.getChatSessions().subscribe({
      next: (s) => this.sessions.set(s),
      error: (e) => console.error(e)
    });

  }

  loadChatHistory(sessionId: string) {
    this.resourceService.getChatHistory(sessionId).subscribe({
      next: (h) => this.chat_history.set(h),
      error: (e) => console.error(e)
    });
  }

  selectSession(sessionId: string) {
    this.selectedSessionId.set(sessionId);
    this.isMessageOpen.set(true);
    this.loadChatHistory(sessionId);
    sessionStorage.setItem('chat_session_id', sessionId);
  }

  goBack() {
    this.selectedSessionId.set(null);
    this.isMessageOpen.set(false);
    this.chat_history.set([]);
    sessionStorage.removeItem('chat_session_id');
  }

  getChatCompletions(userInput: string) {
    if (!userInput.trim()) return;

    const outgoingSessionId = this.selectedSessionId() || '';

    this.chat_history.update((h) => [
      ...h,
      {
        session_id: outgoingSessionId,
        role: 'user',
        message: userInput,
        courses: null,
        timestamp: new Date().toISOString()
      }
    ]);
    this.text_input.set('');

    this.resourceService.chat(userInput, outgoingSessionId).subscribe({
      next: (res: ChatResourceResponse) => {
        this.selectedSessionId.set(res.session_id);
        sessionStorage.setItem('chat_session_id', res.session_id);

        this.chat_history.update((h) => [
          ...h,
          {
            session_id: res.session_id,
            role: 'assistant',
            message: res.message,
            courses: res.courses,
            timestamp: new Date().toISOString()
          }
        ]);

        this.loadChatSessions();
      },
      error: (e) => console.error('chat error', e)
    });
  }

  toggleChatWindow() {
    this.chatService.toggleChatWindow();
  }

  openDialog(courseCards: CourseSeekCourse[]) {
    this.dialog.open(ShowCourseseekCardsComponent, {
      data: courseCards
    });
  }
}
