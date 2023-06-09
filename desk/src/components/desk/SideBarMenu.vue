<template>
	<div
		class="flex w-56 shrink select-none flex-col border-r text-base text-gray-700"
	>
		<div>
			<Dropdown class="p-2" :options="profileSettings">
				<template #default="{ open }">
					<Button
						appearance="minimal"
						class="py-2 pl-2"
						:label="authStore.userName"
						:icon-right="open ? 'chevron-up' : 'chevron-down'"
					>
						<template #icon-left>
							<Avatar
								size="sm"
								class="mr-2"
								:label="authStore.userName"
								:image-u-r-l="authStore.userImage"
							/>
						</template>
					</Button>
				</template>
			</Dropdown>
		</div>
		<div class="flex flex-col gap-1 px-2">
			<div
				v-for="option in menuOptions"
				:key="option.label"
				class="flex cursor-pointer items-center gap-2 rounded-lg px-2 py-1"
				:class="{
					'bg-gray-200': isActive(option.label),
					'text-gray-900': isActive(option.label),
					'hover:bg-gray-300': isActive(option.label),
					'hover:bg-gray-100': !isActive(option.label),
				}"
				@click="$router.push(option.to)"
			>
				<component :is="option.icon_"></component>
				<div>
					{{ option.label }}
				</div>
			</div>
		</div>
		<div class="grow"></div>
		<div class="mb-3 flex flex-col gap-1 px-2">
			<div
				v-for="option in footerOptions"
				:key="option.label"
				class="flex cursor-pointer items-center gap-2 rounded-lg px-2 py-1"
				:class="{
					'bg-gray-200': isActive(option.label),
					'text-gray-900': isActive(option.label),
					'hover:bg-gray-300': isActive(option.label),
					'hover:bg-gray-100': !isActive(option.label),
				}"
				@click="$router.push(option.to)"
			>
				<component :is="option.icon_"></component>
				<div>
					{{ option.label }}
				</div>
			</div>
		</div>
		<Dialog
			v-model="showKeyboardShortcuts"
			:options="{ title: 'Keyboard Shortcuts' }"
		>
			<template #body-content>
				<div class="py-5 text-base">
					<table class="w-full table-fixed border-collapse border">
						<tbody>
							<tr
								v-for="shortcut in keyboardShortcuts"
								:key="shortcut.label"
								class="h-16 border-y"
							>
								<td class="w-28 border-r px-4">
									<span
										class="rounded bg-gray-100 p-1.5 text-gray-500 shadow shadow-gray-400"
									>
										{{ shortcut.sequence }}
									</span>
								</td>
								<td class="px-4">{{ shortcut.label }}</td>
							</tr>
						</tbody>
					</table>
				</div>
			</template>
		</Dialog>
	</div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useRoute } from "vue-router";
import { Dropdown, Avatar } from "frappe-ui";
import { useAuthStore } from "@/stores/auth";
import IconDashboard from "@/assets/icons/dashboard.svg?component";
import IconTicket from "@/assets/icons/ticket.svg?component";
import IconCustomer from "@/assets/icons/customer.svg?component";
import IconContact from "@/assets/icons/contact.svg?component";
import IconKnowledgeBase from "@/assets/icons/knowledge-base.svg?component";
import IconSettings from "@/assets/icons/settings.svg?component";

const route = useRoute();
const authStore = useAuthStore();
const isMac = navigator.userAgent.indexOf("Mac OS X") != -1;
const showKeyboardShortcuts = ref(false);

const keyboardShortcuts = [
	{
		sequence: isMac ? "⌃ + ⌥ + R" : "Ctrl + Alt + R",
		label: "Mark status of ticket as Replied",
	},
	{
		sequence: isMac ? "⌃ + ⌥ + E" : "Ctrl + Alt + E",
		label: "Mark status of ticket as Resolved",
	},
	{
		sequence: isMac ? "⌃ + ⌥ + C" : "Ctrl + Alt + C",
		label: "Mark status of ticket as Closed",
	},
];

const menuOptions = [
	{
		label: "Dashboard",
		icon_: IconDashboard,
		to: {
			name: "Dashboard",
		},
	},
	{
		label: "Tickets",
		icon_: IconTicket,
		to: {
			name: "DeskTickets",
		},
	},
	{
		label: "Customers",
		icon_: IconCustomer,
		to: {
			name: "Customers",
		},
	},
	{
		label: "Contacts",
		icon_: IconContact,
		to: {
			name: "Contacts",
		},
	},
];

const footerOptions = [
	{
		label: "Knowledge Base",
		icon_: IconKnowledgeBase,
		to: {
			name: "DeskKBHome",
		},
	},
	{
		label: "Settings",
		icon_: IconSettings,
		to: {
			name: "Settings",
		},
	},
];

const profileSettings = [
	{
		label: "Shortcuts",
		icon: "command",
		handler: () => {
			showKeyboardShortcuts.value = true;
		},
	},
	{
		label: "Customer portal",
		icon: "users",
		handler: () => {
			window.open("/my-tickets", "_blank");
		},
	},
	{
		label: "Log out",
		icon: "log-out",
		handler: () => authStore.logout(),
	},
];

const routeMap = {
	"Knowledge Base": "/kb",
	Contacts: "/contacts",
	Customers: "/customers",
	Dashboard: "/dashboard",
	Reports: "/reports",
	Settings: "/settings",
	Tickets: "/tickets",
};

function isActive(label: string) {
	return route.path.includes(routeMap[label]);
}
</script>
