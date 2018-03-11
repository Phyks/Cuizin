<template>
    <v-container text-xs-center v-if="isImporting">
        <v-layout row wrap>
            <Loader></Loader>

            <v-flex xs12>
                <p>{{ $t('new.importing') }}</p>
            </v-flex>
        </v-layout>
    </v-container>
    <v-container text-xs-center v-else class="panel">
        <v-layout row wrap>
            <ImportForm v-model="isImporting"></ImportForm>
        </v-layout>
        <v-layout row wrap mt-5>
            <EditForm v-model="isImporting"></EditForm>
        </v-layout>
    </v-container>
</template>

<script>
import EditForm from '@/components/EditForm';
import ImportForm from '@/components/ImportForm';
import Loader from '@/components/Loader';


export default {
    components: {
        EditForm,
        ImportForm,
        Loader,
    },
    data() {
        return {
            isImporting: false,
        };
    },
};
</script>
