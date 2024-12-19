import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ExampleLinechartsComponent } from './example-linecharts.component';

describe('ExampleLinechartsComponent', () => {
  let component: ExampleLinechartsComponent;
  let fixture: ComponentFixture<ExampleLinechartsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ExampleLinechartsComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(ExampleLinechartsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
