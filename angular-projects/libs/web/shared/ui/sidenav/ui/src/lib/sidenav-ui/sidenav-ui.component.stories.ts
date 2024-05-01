import type { Meta, StoryObj } from '@storybook/angular';
import { SidenavUiComponent } from './sidenav-ui.component';

import { within } from '@storybook/testing-library';
import { expect } from '@storybook/jest';

const meta: Meta<SidenavUiComponent> = {
  component: SidenavUiComponent,
  title: 'SidenavUiComponent',
};
export default meta;
type Story = StoryObj<SidenavUiComponent>;

export const Primary: Story = {
  args: {},
};

export const Heading: Story = {
  args: {},
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    expect(canvas.getByText(/sidenav-ui works!/gi)).toBeTruthy();
  },
};
