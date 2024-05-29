import { ComponentFixture, TestBed } from '@angular/core/testing';
import { PlaygroundUiComponent } from './playground-ui.component';

describe('PlaygroundUiComponent', () => {
  let component: PlaygroundUiComponent;
  let fixture: ComponentFixture<PlaygroundUiComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PlaygroundUiComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(PlaygroundUiComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
