package cn.edu.tsinghua.thss.popcorn;

import android.app.ActionBar;
import android.app.Activity;
import android.app.ListActivity;
import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.Button;
import android.widget.DatePicker;
import android.widget.ListView;
import android.widget.TextView;

import com.beardedhen.androidbootstrap.FontAwesomeText;
import com.lidroid.xutils.ViewUtils;
import com.lidroid.xutils.view.annotation.ViewInject;
import com.lidroid.xutils.view.annotation.event.OnClick;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;


public class RankActivity extends Activity {

    private List<Map<String, Object>> mData = null;

    private RankListAdapter adapter;

    @ViewInject(R.id.rank_datepicker)
    private DatePicker datePicker;

    @ViewInject(R.id.rank_submit_date)
    private Button submitDate;

    @ViewInject(R.id.rank_listview)
    private ListView lv ;

    @OnClick(R.id.rank_submit_date)
    private void submitDataClick(View v){
        String[] str_name = {"黄小明","王小明","小明","赵小明","孙小明"};
        String[] str_dept = {"微谷项目部","天坛项目部","天坛项目部","微谷项目部","微谷项目部"};
        String[] str_credit = {"140","120","110","90","80"};
        mData = getData(str_name, str_dept, str_credit);
        adapter.notifyDataSetChanged();
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_rank);

        ViewUtils.inject(this);

        if (datePicker != null) {
            ((ViewGroup)((ViewGroup) datePicker.getChildAt(0)).getChildAt(0)).getChildAt(2).setVisibility(View.GONE);
        }

        String[] str_name = {"黄小明","王小明","小明","赵小明","孙小明","钱小明","李小明","李小明","李小明"};
        String[] str_dept = {"微谷项目部","天坛项目部","天坛项目部","微谷项目部","微谷项目部","微谷项目部","微谷项目部","天坛项目部","天坛项目部"};
        String[] str_credit = {"140","120","110","90","80","60","50","50","50"};
        mData = getData(str_name, str_dept, str_credit);

        adapter = new RankListAdapter (this);
        lv.setAdapter(adapter);

    }

    private List<Map<String, Object>> getData(String[] str_name, String[] str_dept, String[] str_credit) {
        List<Map<String ,Object>> list = new ArrayList<Map<String,Object>>();

        for (int i = 0; i < str_dept.length; i++) {
            Map<String, Object> map = new HashMap<String, Object>();
            map.put("name", str_name[i]);
            map.put("dept", str_dept[i]);
            map.put("credit", str_credit[i]);
            list.add(map);
        }

        return list;
    }

    class ViewHolder {
        public TextView name;
        public TextView dept;
        public TextView credit;
    }

    public class RankListAdapter extends BaseAdapter {
        private LayoutInflater mInflater = null;

        public RankListAdapter(Context context) {
            super();
            mInflater = (LayoutInflater) context
                    .getSystemService(Context.LAYOUT_INFLATER_SERVICE);
        }

        @Override
        public int getCount() {
            if (mData == null){
                return 0;
            }else{
                return mData.size();
            }
        }

        @Override
        public Object getItem(int position) {
            // TODO Auto-generated method stub
            return null;
        }

        @Override
        public long getItemId(int position) {
            // TODO Auto-generated method stub
            return position;
        }

        @Override
        public View getView(int position, View convertView, ViewGroup parent) {

            ViewHolder holder = null;
            if (convertView == null) {
                holder = new ViewHolder();
                convertView = mInflater.inflate(R.layout.listview_rank, null);

                holder.name = (TextView) convertView.findViewById(R.id.listview_rank_name);
                holder.dept = (TextView) convertView.findViewById(R.id.listview_rank_dept);
                holder.credit = (TextView) convertView.findViewById(R.id.listview_rank_credit);
                convertView.setTag(holder);
            } else {
                holder = (ViewHolder) convertView.getTag();
            }

            holder.name.setText((String)mData.get(position).get("name"));
            holder.dept.setText((String)mData.get(position).get("dept"));
            holder.credit.setText((String)mData.get(position).get("credit"));

            return convertView;
        }
    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.rank, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();
        if (id == R.id.close_btn) {
            RankActivity.this.finish();
            return true;
        }
        return super.onOptionsItemSelected(item);
    }
}
