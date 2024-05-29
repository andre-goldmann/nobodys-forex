import { ComponentFixture, TestBed } from '@angular/core/testing';
import { SignalsUiComponent } from './signals-ui.component';

describe('SignalsUiComponent', () => {
  let component: SignalsUiComponent;
  let fixture: ComponentFixture<SignalsUiComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SignalsUiComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(SignalsUiComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
