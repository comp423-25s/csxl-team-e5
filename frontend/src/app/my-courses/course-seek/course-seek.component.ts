import { Component, Input, signal, WritableSignal } from '@angular/core';
import { ChatResourceResponse, CourseSeekService } from './course-seek.service';
import { map } from 'rxjs';

interface ChatHistory extends ChatResourceResponse {
  role: "Assistant" | "User"
}

@Component({
  selector: 'app-course-seek',
  templateUrl: './course-seek.component.html',
  styleUrl: './course-seek.component.css'
})
export class CourseSeekComponent {
  text_input: WritableSignal<string> = signal('');
  chat_history: WritableSignal<ChatHistory[]> = signal([])

  constructor(private resourceService: CourseSeekService) {}

  async getChatCompletions(user_input: string) {
    const courseSeekResponse = await this.resourceService.chat(user_input)
    const toChatHistory = (response: ChatResourceResponse) => {
      return {
        ...response,
        role: "Assistant"
      } as ChatHistory
    }
    courseSeekResponse.pipe(map((response) => this.chat_history.set([...this.chat_history(), toChatHistory(response)]))).subscribe()
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
