import { Component, OnInit, signal, WritableSignal } from '@angular/core';
import { ChatResourceResponse, CourseSeekService, SessionResourceResponse } from './course-seek.service';
import { map } from 'rxjs';
import { ChatService } from 'src/app/shared/chat-service/chat-service';
import { CourseSiteOverview } from '../my-courses.model';
import { MatDialog } from '@angular/material/dialog';
import { ShowCourseseekCardsComponent } from '../dialogs/show-courseseek-cards/show-courseseek-cards.component';
import { v4 as uuidv4 } from 'uuid';


interface ChatHistory extends ChatResourceResponse {
  role: 'assistant' | 'user';
}
export interface CourseSeekCourseCard {
  course: CourseSiteOverview;
  termId: string;
}

@Component({
  selector: 'app-course-seek',
  templateUrl: './course-seek.component.html',
  styleUrl: './course-seek.component.css'
})
export class CourseSeekComponent implements OnInit {
  isMessageOpen: WritableSignal<boolean> = signal(false);
  text_input: WritableSignal<string> = signal('');
  sessions: WritableSignal<SessionResourceResponse[]> = signal([]);
  selectedSessionId: WritableSignal<string | null> = signal(null);
  chat_history: WritableSignal<ChatHistory[]> = signal([]);
  default_msg: WritableSignal<ChatHistory> = signal({
    role: 'assistant',
    message: 'Hi, I am CourseSeek. How can I help you today?',
    sections: null
  });

  exampleCourseData = {
    course: {
      id: 12345,
      term_id: 'SP2025',
      subject_code: 'COMP',
      number: '426',
      title: 'Modern Web Programming',
      role: 'instructor',
      sections: [
        {
          id: 10001,
          number: '001',
          meeting_pattern: 'MWF 10:00AM-10:50AM, SN 011',
          course_site_id: 12345,
          subject_code: 'COMP',
          course_number: '426',
          section_number: '001'
        },
        {
          id: 10002,
          number: '601',
          meeting_pattern: 'Th 3:30PM-4:45PM, SN 115',
          course_site_id: 12345,
          subject_code: 'COMP',
          course_number: '426',
          section_number: '601'
        }
      ],
      gtas: [
        {
          id: 2001,
          onyen: 'gradta1',
          first_name: 'Graduate',
          last_name: 'Assistant',
          pronouns: 'they/them',
          email: 'gradta1@unc.edu',
          github_avatar: 'https://github.com/avatars/gradta1.jpg',
          github: 'gradta1',
          bio: 'Computer Science PhD student focusing on web technologies.',
          linkedin: 'https://linkedin.com/in/gradta1',
          website: 'https://cs.unc.edu/~gradta1'
        }
      ],
      utas: [
        {
          id: 3001,
          onyen: 'undergradta1',
          first_name: 'Undergraduate',
          last_name: 'Assistant1',
          pronouns: 'she/her',
          email: 'undergradta1@unc.edu',
          github_avatar: 'https://github.com/avatars/undergradta1.jpg',
          github: 'undergradta1',
          bio: 'Senior Computer Science major, passionate about teaching.',
          linkedin: 'https://linkedin.com/in/undergradta1',
          website: null
        },
        {
          id: 3002,
          onyen: 'undergradta2',
          first_name: 'Undergraduate',
          last_name: 'Assistant2',
          pronouns: 'he/him',
          email: 'undergradta2@unc.edu',
          github_avatar: 'https://github.com/avatars/undergradta2.jpg',
          github: 'undergradta2',
          bio: 'Junior CS & Math double major who loves frontend development.',
          linkedin: null,
          website: 'https://undergradta2.github.io'
        }
      ]
    },
    termId: 'SP2025'
  };
  courseCardArray: WritableSignal<CourseSeekCourseCard[]> = signal([
    this.exampleCourseData,
    this.exampleCourseData,
    this.exampleCourseData,
    this.exampleCourseData,
    this.exampleCourseData,
    this.exampleCourseData,
    this.exampleCourseData,
    this.exampleCourseData,
    this.exampleCourseData
  ]);

  constructor(
    private resourceService: CourseSeekService,
    protected chatService: ChatService,
    private dialog: MatDialog
  ) {}

  ngOnInit(): void {
    this.loadChatSessions();
  }

  public sessionId: string =
    sessionStorage.getItem('chat_session_id') || uuidv4();
    
    loadChatSessions() {
      // Comment out the API call temporarily
      /*
      this.resourceService.getChatSessions().subscribe({
        next: (sessions: SessionResourceResponse[]) => {
          this.sessions.set(sessions);
        },
        error: (error) => {
          console.error(`Error loading chat sessions: ${error}`);
        }
      });
      */
      
      // Add fake sessions data
      const fakeSessions: SessionResourceResponse[] = [
        {
          session_id: '1234-abcd-5678-efgh',
          latest_message: {
            role: 'assistant',
            message: 'I found COMP 426 Modern Web Programming. It meets MWF 10:00AM-10:50AM in SN 011 and has a recitation on Thursdays.',
            sections: null
          }
        },
        {
          session_id: '5678-ijkl-9012-mnop',
          latest_message: {
            role: 'assistant',
            message: 'Professor Kris Jordan teaches COMP 426. The course has 2 GTAs and 3 UTAs who hold office hours throughout the week.',
            sections: null
          }
        },
        {
          session_id: '9012-qrst-3456-uvwx',
          latest_message: {
            role: 'user',
            message: 'When is the final exam for COMP 426?',
            sections: null
          }
        },
        {
          session_id: '7890-yzab-1234-cdef',
          latest_message: {
            role: 'assistant',
            message: 'The deadline for the final project has been extended to May 5th at 11:59 PM. Make sure to submit through the course website.',
            sections: null
          }
        },
        {
          session_id: '4321-ghij-8765-klmn',
          latest_message: {
            role: 'assistant',
            message: 'You can find all the lecture materials and assignment instructions in the Resources section of the course website.',
            sections: null
          }
        },
        {
          session_id: '4321-ghij-8765-klmn',
          latest_message: {
            role: 'assistant',
            message: 'You can find all the lecture materials and assignment instructions in the Resources section of the course website.',
            sections: null
          }
        }
      ];
      
      this.sessions.set(fakeSessions);
    }
  
    loadChatHistory(sessionId: string) {
      // Comment out the API call temporarily
      /*
      this.resourceService.getChatHistory(sessionId).subscribe({
        next: (history: ChatHistoryResponse[]) => {
          this.chat_history.set(history);
        },
        error: (error) => {
          console.error('Error loading chat history: ', error);
        }
      });
      */
      
      // Add fake chat history based on sessionId
      const fakeChatHistories: { [key: string]: ChatHistory[] } = {
        '1234-abcd-5678-efgh': [
          {
            role: 'user',
            message: 'Can you tell me about COMP 426?',
            sections: null
          },
          {
            role: 'assistant',
            message: 'COMP 426 is Modern Web Programming, a course that teaches frontend and backend development using JavaScript frameworks.',
            sections: null
          },
          {
            role: 'user',
            message: 'When and where does it meet?',
            sections: null
          },
          {
            role: 'assistant',
            message: 'I found COMP 426 Modern Web Programming. It meets MWF 10:00AM-10:50AM in SN 011 and has a recitation on Thursdays.',
            sections: null
          }
        ],
        '5678-ijkl-9012-mnop': [
          {
            role: 'user',
            message: 'Who teaches COMP 426?',
            sections: null
          },
          {
            role: 'assistant',
            message: 'Professor Kris Jordan teaches COMP 426. The course has 2 GTAs and 3 UTAs who hold office hours throughout the week.',
            sections: null
          }
        ],
        '9012-qrst-3456-uvwx': [
          {
            role: 'user',
            message: 'When is the final exam for COMP 426?',
            sections: null
          }
        ],
        '7890-yzab-1234-cdef': [
          {
            role: 'user',
            message: 'Has the deadline for the final project been extended?',
            sections: null
          },
          {
            role: 'assistant',
            message: 'The deadline for the final project has been extended to May 5th at 11:59 PM. Make sure to submit through the course website.',
            sections: null
          }
        ],
        '4321-ghij-8765-klmn': [
          {
            role: 'user',
            message: 'Where can I find the lecture materials?',
            sections: null
          },
          {
            role: 'assistant',
            message: 'You can find all the lecture materials and assignment instructions in the Resources section of the course website.',
            sections: null
          }
        ]
      };
      
      // Set the chat history based on the selected session
      if (fakeChatHistories[sessionId]) {
        this.chat_history.set(fakeChatHistories[sessionId]);
      } else {
        this.chat_history.set([]);
      }
    }
  
    selectSession(sessionId: string) {
      this.selectedSessionId.set(sessionId);
      this.isMessageOpen.set(true);
      this.loadChatHistory(sessionId);
    }
  
    goBack() {
      this.selectedSessionId.set(null);
      this.isMessageOpen.set(false);
      this.chat_history.set([]);
    }
  
    startNewChat() {
      const newSessionId = uuidv4();
      this.selectedSessionId.set(newSessionId);
      this.isMessageOpen.set(true);
      this.chat_history.set([])

      sessionStorage.setItem('chat_session_id', newSessionId);
    }
  
    getChatCompletions(userInput: string) {
      if (!userInput.trim()) return;
      
      if (!this.selectedSessionId() && this.isMessageOpen()) {
        this.chat_history.update(history => [
          ...history,
          { role: 'user', message: userInput, sections: null }
        ]);
        
        this.text_input.set('');
        
        this.resourceService.chat(userInput, '')
          .pipe(
            map((response) => {
              this.chat_history.update(history => [
                ...history, 
                { ...response, role: 'assistant' }
              ]);
              
              this.loadChatSessions();

              return response;
            })
          )
          .subscribe({
            error: (error) => {
              console.error('Error creating new chat session:', error);
            }
          });
      } else if (this.selectedSessionId()) {
        const sessionId = this.selectedSessionId() as string;
        
        this.chat_history.update(history => [
          ...history,
          { role: 'user', message: userInput, sections: null }
        ]);
        
        this.text_input.set('');
        
        this.resourceService.chat(userInput, sessionId)
          .pipe(
            map((response) => 
              this.chat_history.update(history => [
                ...history, 
                { ...response, role: 'assistant' }
              ])
            )
          )
          .subscribe({
            next: () => {
              this.loadChatSessions();
            },
            error: (error) => {
              console.error('Error sending message:', error);
            }
          });
      }
    }

  toggleChatWindow() {
    this.chatService.toggleChatWindow();
  }

  openDialog(courseCardArray: CourseSeekCourseCard[]) {
    this.dialog.open(ShowCourseseekCardsComponent, {
      data: courseCardArray
    });
  }
}
