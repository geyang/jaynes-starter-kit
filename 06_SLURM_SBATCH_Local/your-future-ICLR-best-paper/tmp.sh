#!/bin/bash
# to allow process substitution
set +o posix
mkdir -p ~/debug-outputs
JAYNES_LOG_DIR=~/debug-outputs
{
    # clear main_log
    truncate -s 0 ~/debug-outputs/jaynes-launch.log
    truncate -s 0 ~/debug-outputs/jaynes-launch.err.log


    if ! type aws > /dev/null; then
        pip install awscli --upgrade --user
    fi



    # remote_setup

    # upload_script


    # todo: include this inside the runner script.

    cd /Users/geyang/fair/learnfair-starter-kit/code/your-future-ICLR-best-paper/sandbox
    cat >/tmp/jaynes-batch-script-etw_debug-03.47.26.632714.sh <<EOL 
            #!/bin/bash
#SBATCH --output=/checkpoint/%u/jobs/job.%j.out
#SBATCH --error=/checkpoint/%u/jobs/job.%j.err
#SBATCH --job-name etw_debug-03.47.26.632714
#SBATCH --nodes 1
#SBATCH --time=6:0:0
#SBATCH --signal=USR1@600
#SBATCH --cpus-per-task 10
#SBATCH --mem-per-cpu 5625MB
#SBATCH --partition dev
#SBATCH --open-mode=append#SBATCH --gres gpu:1
#SBATCH --ntasks-per-node 1
export LC_CTYPE=en_US.UTF-8
cd '/Users/geyang/fair/learnfair-starter-kit/code/your-future-ICLR-best-paper';LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu/nvidia-openglsource /private/home/erikwijmans/miniconda3/etc/profile.d/conda.sh
conda activate jaynes
export MASTER_ADDR=\$(srun --ntasks=1 hostname 2>&1 | tail -n1)
export PYTHONPATH=/tmp/a3ed55e2-d885-43c2-a057-8e2e9cbeb55b{JAYNES_PARAMS_KEY=${1} srun python -u -m jaynes.entry}> >(tee -a ${JAYNES_LOG_DIR}/etw_debug-03.47.26.632714.log) 2> >(tee -a ${JAYNES_LOG_DIR}/etw_debug-03.47.26.632714.err.log >&2)
EOL

    sbatch /tmp/jaynes-batch-script-etw_debug-03.47.26.632714.sh gASVOggAAAAAAAB9lCiMBXRodW5rlIwXY2xvdWRwaWNrbGUuY2xvdWRwaWNrbGWUjA5fZmlsbF9mdW5jdGlvbpSTlChoAowPX21ha2Vfc2tlbF9mdW5jlJOUaAKMDV9idWlsdGluX3R5cGWUk5SMCENvZGVUeXBllIWUUpQoSwBLAEsBSwJLQ0MQZAF9AHQAfACDAQEAZABTAJROWP4FAAAKICAgICMgVGhlIEF3ZXNvbWUgTUwtTG9nZ2VyCiAgICAKICAgIFlvdSBjYW4gcnVuIHRoZSBmb2xsb3dpbmcgY29kZSB3aXRoIG1sLWxvZ2dlcjoKICAgIAogICAgYGBgcHl0aG9uCiAgICBmcm9tIG1sX2xvZ2dlciBpbXBvcnQgbG9nZ2VyCiAgICAKICAgIGxvZ2dlci5sb2cobHI9MCwgY2xpcCByYW5nZT0wLjIwMCwgc3RlcD0wLCB0aW1lc3RhbXA9JzIwMTgtMTEtMTZUMDA6MDk6MjcuMTk4MTQyJywgcmV3YXJkPS0xMDkuNDMpCiAgICBsb2dnZXIuZmx1c2goKQogICAgYGBgCiAgICDilZLilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilaTilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilZDilZUKICAgIOKUgiAgICAgICAgIGxyICAgICAgICAg4pSCICAgICAgICAgICAwLjAwMCAgICAgICAgICAgIOKUggogICAg4pSc4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pS84pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSkCiAgICDilIIgICAgIGNsaXAgcmFuZ2UgICAgIOKUgiAgICAgICAgICAgMC4yMDAgICAgICAgICAgICDilIIKICAgIOKUnOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUvOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUgOKUpAogICAg4pSCICAgICAgICBzdGVwICAgICAgICDilIIgICAgICAgICAgICAgMCAgICAgICAgICAgICAg4pSCCiAgICDilJzilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilLzilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilKQKICAgIOKUgiAgICAgIHRpbWVzdGFtcCAgICAg4pSCJzIwMTgtMTEtMTZUMDA6MDk6MjcuMTk4MTQyJ+KUggogICAg4pSc4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pS84pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSkCiAgICDilIIgICAgICAgcmV3YXJkICAgICAgIOKUgiAgICAgICAgICAtMTA5LjQzICAgICAgICAgICDilIIKICAgIOKVmOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVp+KVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVkOKVmwogICAglIaUjAVwcmludJSFlIwBc5SFlIxZL1VzZXJzL2dleWFuZy9mYWlyL2xlYXJuZmFpci1zdGFydGVyLWtpdC9jb2RlL3lvdXItZnV0dXJlLUlDTFItYmVzdC1wYXBlci9sYXVuY2hfZW50cnkucHmUjAZsYXVuY2iUSwVDBAAXBAGUKSl0lFKUSv////99lCiMC19fcGFja2FnZV9flE6MCF9fbmFtZV9flIwIX19tYWluX1+UjAhfX2ZpbGVfX5SMWS9Vc2Vycy9nZXlhbmcvZmFpci9sZWFybmZhaXItc3RhcnRlci1raXQvY29kZS95b3VyLWZ1dHVyZS1JQ0xSLWJlc3QtcGFwZXIvbGF1bmNoX2VudHJ5LnB5lHWHlFKUfZQojAdnbG9iYWxzlH2UjAhkZWZhdWx0c5ROjARkaWN0lH2UjA5jbG9zdXJlX3ZhbHVlc5ROjAZtb2R1bGWUaBuMBG5hbWWUaBSMA2RvY5ROjAthbm5vdGF0aW9uc5R9lIwIcXVhbG5hbWWUaBR1dFKMBGFyZ3OUKYwGa3dhcmdzlH2UdS4=tail -f ${JAYNES_LOG_DIR}/etw_debug-03.47.26.632714.log ${JAYNES_LOG_DIR}/etw_debug-03.47.26.632714.err.log

    # todo: consider saving this in a mounted directory instead.
    cat /tmp/jaynes-batch-script-etw_debug-03.47.26.632714.sh
    rm /tmp/jaynes-batch-script-etw_debug-03.47.26.632714.sh



} > >(tee -a ~/debug-outputs/jaynes-launch.log) 2> >(tee -a ~/debug-outputs/jaynes-launch.err.log >&2)