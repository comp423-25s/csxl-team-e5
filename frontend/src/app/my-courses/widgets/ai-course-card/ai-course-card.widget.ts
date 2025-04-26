import { Component, Input } from '@angular/core';
import { CourseSiteOverview } from '../../my-courses.model';

@Component({
  selector: 'ai-course-card',
  templateUrl: './ai-course-card.widget.html',
  styleUrls: ['./ai-course-card.widget.scss']
})
export class AICourseCardWidget {
  @Input() courseNumber!: string;
  @Input() courseTitle!: string;
  @Input() credits!: string;
  @Input() description!: string;
  @Input() requirements!: string;
  constructor() {}
}
