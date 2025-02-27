import { ComponentFixture, TestBed } from '@angular/core/testing';
import { SidenavBodyComponent } from './sidenav-body.component';

describe('SidenavBodyComponent', () => {
  let component: SidenavBodyComponent;
  let fixture: ComponentFixture<SidenavBodyComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SidenavBodyComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(SidenavBodyComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
