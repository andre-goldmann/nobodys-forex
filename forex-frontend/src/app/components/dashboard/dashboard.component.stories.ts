import type { Meta, StoryObj } from '@storybook/angular';

import { argsToTemplate } from '@storybook/angular';

import { action } from '@storybook/addon-actions';
import {DashboardComponent} from "./dashboard.component";

export const actionsData = {
  login: action('login'),
  //onArchiveTask: action('onArchiveTask'),
};

const meta: Meta<DashboardComponent> = {
  title: 'Dashboard',
  component: DashboardComponent,
  /*argTypes: {
    variant: {
      options: ['primary', 'secondary'],
      control: { type: 'radio' },
    },
  },*/
  excludeStories: /.*Data$/,
  tags: ['autodocs'],
  render: (args: DashboardComponent) => ({
    props: {
      ...args,
      login: actionsData.login,
      //onArchiveTask: actionsData.onArchiveTask,
    },
    template: `<app-dashboard ${argsToTemplate(args)}></app-dashboard>`,
  }),
};

export default meta;
type Story = StoryObj<DashboardComponent>;

export const Default: Story = {
  args: {
    /*task: {
      id: '1',
      title: 'Test Task',
      state: 'TASK_INBOX',
    },*/
  },
};

export const Pinned: Story = {
  args: {
    /*task: {
      ...Default.args?.task,
      state: 'TASK_PINNED',
    },*/
  },
};

export const Archived: Story = {
  args: {
    /*task: {
      ...Default.args?.task,
      state: 'TASK_ARCHIVED',
    },*///
  },
};
