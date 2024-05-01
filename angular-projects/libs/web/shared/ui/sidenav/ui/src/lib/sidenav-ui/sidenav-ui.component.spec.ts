import { ComponentFixture, TestBed } from '@angular/core/testing';
import { SidenavUiComponent } from './sidenav-ui.component';

describe('SidenavUiComponent', () => {
  let component: SidenavUiComponent;
  let fixture: ComponentFixture<SidenavUiComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SidenavUiComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(SidenavUiComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
