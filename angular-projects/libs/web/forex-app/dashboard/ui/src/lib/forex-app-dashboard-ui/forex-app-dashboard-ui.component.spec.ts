import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ForexAppDashboardUiComponent } from './forex-app-dashboard-ui.component';

describe('ForexAppDashboardUiComponent', () => {
  let component: ForexAppDashboardUiComponent;
  let fixture: ComponentFixture<ForexAppDashboardUiComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ForexAppDashboardUiComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(ForexAppDashboardUiComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
