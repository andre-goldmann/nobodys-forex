import type { Meta, StoryObj } from '@storybook/angular';
import { ForexAppDashboardUiComponent } from './forex-app-dashboard-ui.component';

import { within } from '@storybook/testing-library';
import { expect } from '@storybook/jest';

const meta: Meta<ForexAppDashboardUiComponent> = {
  component: ForexAppDashboardUiComponent,
  title: 'ForexAppDashboardUiComponent',
};
export default meta;
type Story = StoryObj<ForexAppDashboardUiComponent>;

export const Primary: Story = {
  args: {},
};
//
export const Heading: Story = {
  args: {},
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    expect(canvas.getByText(/forex-app-dashboard-ui works!/gi)).toBeTruthy();
  },
};
