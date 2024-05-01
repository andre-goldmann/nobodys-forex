import { ComponentFixture, TestBed } from '@angular/core/testing';
import { FdaDashboardUiComponent } from './fda-dashboard-ui.component';

describe('FdaDashboardUiComponent', () => {
  let component: FdaDashboardUiComponent;
  let fixture: ComponentFixture<FdaDashboardUiComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FdaDashboardUiComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(FdaDashboardUiComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
