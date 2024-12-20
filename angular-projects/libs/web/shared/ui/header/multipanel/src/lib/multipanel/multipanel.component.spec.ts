import { ComponentFixture, TestBed } from '@angular/core/testing';
import { MultipanelComponent } from './multipanel.component';

describe('MultipanelComponent', () => {
  let component: MultipanelComponent;
  let fixture: ComponentFixture<MultipanelComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MultipanelComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(MultipanelComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
