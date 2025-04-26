import { Component, Inject } from '@angular/core';
import { CourseSeekCourseCard } from '../../course-seek/course-seek.component';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';
import { CourseSeekCourse } from '../../course-seek/models';

@Component({
  selector: 'app-show-courseseek-cards',
  templateUrl: './show-courseseek-cards.component.html',
  styleUrl: './show-courseseek-cards.component.css'
})
export class ShowCourseseekCardsComponent {
  constructor(@Inject(MAT_DIALOG_DATA) public courses: CourseSeekCourse[]) {}
}
