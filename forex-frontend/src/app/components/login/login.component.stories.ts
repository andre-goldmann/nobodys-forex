import type { Meta, StoryObj } from '@storybook/angular';

import { argsToTemplate } from '@storybook/angular';

import { action } from '@storybook/addon-actions';
import LoginComponent from "./login.component";


export const actionsData = {
  login: action('login'),
  //onArchiveTask: action('onArchiveTask'),
};

const meta: Meta<LoginComponent> = {
  title: 'Login',
  component: LoginComponent,
  /*argTypes: {
    variant: {
      options: ['primary', 'secondary'],
      control: { type: 'radio' },
    },
  },*/
  excludeStories: /.*Data$/,
  tags: ['autodocs'],
  render: (args: LoginComponent) => ({
    props: {
      ...args,
      login: actionsData.login,
      //onArchiveTask: actionsData.onArchiveTask,
    },
    template: `<app-login ${argsToTemplate(args)}></app-login>`,
  }),
};

export default meta;
type Story = StoryObj<LoginComponent>;

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
