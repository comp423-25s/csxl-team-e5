import { TestBed } from '@angular/core/testing';

import { CourseSeekService } from './course-seek.service';

describe('CourseSeekService', () => {
  let service: CourseSeekService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(CourseSeekService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
