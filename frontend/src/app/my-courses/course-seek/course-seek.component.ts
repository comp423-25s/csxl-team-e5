import { Component, Input, signal, WritableSignal } from '@angular/core';
import { ChatResourceResponse, CourseSeekService } from './course-seek.service';
import { map } from 'rxjs';
import { ChatService } from 'src/app/shared/chat-service/chat-service';

interface ChatHistory extends ChatResourceResponse {
  role: 'assistant' | 'user';
}

@Component({
  selector: 'app-course-seek',
  templateUrl: './course-seek.component.html',
  styleUrl: './course-seek.component.css'
})
export class CourseSeekComponent {
  text_input: WritableSignal<string> = signal('');
  chat_history: WritableSignal<ChatHistory[]> = signal([]);
  default_msg: WritableSignal<ChatHistory> = signal({
    role: 'assistant',
    response: 'Hi, I am CourseSeek. How can I help you today?',
    sections: null
  });

  constructor(private resourceService: CourseSeekService, protected chatService: ChatService) {}

  async getChatCompletions(user_input: string) {
    const courseSeekResponse = await this.resourceService.chat(user_input);
    const toChatHistory = (response: ChatResourceResponse, role: string) => {
      if (role == 'assistant') {
        return {
          ...response,
          role: 'assistant'
        } as ChatHistory;
      } else {
        return {
          ...response,
          role: 'user'
        } as ChatHistory;
      }
    };
    this.chat_history.set([
      ...this.chat_history(),
      toChatHistory(
        {
          sections: null,
          response: user_input
        },
        'user'
      )
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
    this.chatService.toggleChatWindow()
  }
}

// bottom of chat window: input field for text, "send message" button
// chat bubbles for course seek and user, course seek bubbles should be course seek blue #4D6BFE
// meanwhile user bubble should be white/grey
// need to call api for response messages.
// need to save chat history
// (maybe) to have feature to start a new chat? in which case course seek should have a pre-determined first message
// if time permites, course cards similar to the ones alr on the csxl site
// profile image icons (next to chat bubbles) (we alr have a logo for course seek)
