import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CourseSeekComponent } from './course-seek.component';

describe('CourseSeekComponent', () => {
  let component: CourseSeekComponent;
  let fixture: ComponentFixture<CourseSeekComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CourseSeekComponent]
    }).compileComponents();

    fixture = TestBed.createComponent(CourseSeekComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
