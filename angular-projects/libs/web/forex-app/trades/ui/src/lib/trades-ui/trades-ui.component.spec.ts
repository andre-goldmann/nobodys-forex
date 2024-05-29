import { ComponentFixture, TestBed } from '@angular/core/testing';
import { TradesUiComponent } from './trades-ui.component';

describe('TradesUiComponent', () => {
  let component: TradesUiComponent;
  let fixture: ComponentFixture<TradesUiComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TradesUiComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(TradesUiComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
