import { ComponentFixture, TestBed } from '@angular/core/testing';
import { NavBodyComponent } from './nav-body.component';

describe('NavBodyComponent', () => {
  let component: NavBodyComponent;
  let fixture: ComponentFixture<NavBodyComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [NavBodyComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(NavBodyComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
