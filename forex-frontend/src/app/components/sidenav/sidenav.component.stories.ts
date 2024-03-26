import type { Meta, StoryObj } from '@storybook/angular';

import { argsToTemplate } from '@storybook/angular';

import { action } from '@storybook/addon-actions';
import {SidenavComponent} from "./sidenav.component";


export const actionsData = {
  login: action('login'),
  //onArchiveTask: action('onArchiveTask'),
};

const meta: Meta<SidenavComponent> = {
  title: 'Sidenav',
  component: SidenavComponent,
  /*argTypes: {
    variant: {
      options: ['primary', 'secondary'],
      control: { type: 'radio' },
    },
  },*/
  excludeStories: /.*Data$/,
  tags: ['autodocs'],
  render: (args: SidenavComponent) => ({
    props: {
      ...args,
      login: actionsData.login,
      //onArchiveTask: actionsData.onArchiveTask,
    },
    template: `<app-sidenav ${argsToTemplate(args)}></app-sidenav>`,
  }),
};

export default meta;
type Story = StoryObj<SidenavComponent>;

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
