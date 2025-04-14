import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ShowCourseseekCardsComponent } from './show-courseseek-cards.component';

describe('ShowCourseseekCardsComponent', () => {
  let component: ShowCourseseekCardsComponent;
  let fixture: ComponentFixture<ShowCourseseekCardsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ShowCourseseekCardsComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ShowCourseseekCardsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
