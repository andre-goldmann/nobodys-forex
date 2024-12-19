import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ExampleBarchartsComponent } from './example-barcharts.component';

describe('ExampleBarchartsComponent', () => {
  let component: ExampleBarchartsComponent;
  let fixture: ComponentFixture<ExampleBarchartsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ExampleBarchartsComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(ExampleBarchartsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
