import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CourseSeekCourseCard } from '../../course-seek/course-seek.component';
import { CourseSeekCourse } from '../../course-seek/models';

@Component({
  selector: 'chat-bubble',
  templateUrl: './chat-bubble.widget.html',
  styleUrls: ['./chat-bubble.widget.scss']
})
export class ChatBubbleWidget {
  @Input() role!: 'assistant' | 'user';
  @Input() input!: string;
  @Input() courseCardArray!: CourseSeekCourse[] | null;
  @Output() seeCoursesButtonPressed = new EventEmitter<CourseSeekCourse[]>();

  constructor() {}
}
