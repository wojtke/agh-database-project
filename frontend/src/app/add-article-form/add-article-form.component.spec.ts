import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddArticleFormComponent } from './add-article-form.component';

describe('AddArticleFormComponent', () => {
  let component: AddArticleFormComponent;
  let fixture: ComponentFixture<AddArticleFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AddArticleFormComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AddArticleFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
