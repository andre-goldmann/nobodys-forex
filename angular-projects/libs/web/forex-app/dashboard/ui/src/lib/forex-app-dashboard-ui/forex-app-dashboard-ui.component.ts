import {Component, inject} from '@angular/core';
import { CommonModule } from '@angular/common';
import {UserStoreService} from "../../../../../../shared/auth/login/data-access/src/lib/service/user-store.service";

@Component({
  selector: 'lib-forex-app-dashboard-ui',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './forex-app-dashboard-ui.component.html',
  styleUrl: './forex-app-dashboard-ui.component.scss',
})
export class ForexAppDashboardUiComponent {
  protected userStoreService:UserStoreService = inject(UserStoreService);
}
