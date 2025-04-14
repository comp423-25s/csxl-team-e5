import { Component, Input } from '@angular/core';
import { CourseSiteOverview } from '../../my-courses.model';

@Component({
  selector: 'ai-course-card',
  templateUrl: './ai-course-card.widget.html',
  styleUrls: ['./ai-course-card.widget.scss']
})
export class AICourseCardWidget {
  /** Term for the course */
  @Input() termId!: string;
  /** The course to show */
  @Input() course!: CourseSiteOverview;

  constructor() {}
}
